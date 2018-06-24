import ast
from datetime import datetime
from itertools import chain
import numpy as np
import pandas as pd

from pyzoopla.base import BaseProperty
from pyzoopla.utils import currency_to_num, myround, text_inbetween


class PropertyDetails(BaseProperty):
    """
    Details of a property scraped from https://ww2.zoopla.co.uk/property/{property_id}
    """

    def __init__(self, property_id):
        super(PropertyDetails, self).__init__(property_id, slug='property')

    def __str__(self):
        # Address of the property
        return self.soup.find(name='title').text.split(' - ')[0]

    def details(self):
        string = text_inbetween(text=self.html.text.replace('\n', '').replace(' ', ''),
                                left='ZPG.trackData.taxonomy=', right=';</script><script>d')
        string = string.replace('{', '{"').replace(':', '":').replace(',', ',"').replace('null', '"null"')
        return ast.literal_eval(string)

    def location(self):
        string = text_inbetween(text=self.html.text.replace('\n', '').replace(' ', ''),
                                left='"coordinates":', right=',"pin"')
        string = string.replace('false', 'False').replace('true', 'True')
        return ast.literal_eval(string)

    def for_sale(self):
        # current listings available at https://www.zoopla.co.uk/for-sale/details/{listing_id}
        sale = self.soup.find(name='span', attrs={'class': 'pdp-history__details'})
        if sale and sale.text.strip() == 'This property is currently for sale':
            return sale.a['href'].split('/')[-1]
        else:
            return False

    def property_value(self):
        values = [currency_to_num(i.text) for i in
                  self.soup.find_all(name='p', attrs={'class': 'pdp-estimate__price'})]
        ranges = [currency_to_num(i) for i in
                  list(chain(*[i.text[7:].split(' - ')
                               for i in self.soup.find_all(name='p', attrs={'class': 'pdp-estimate__range'})]))]

        try:
            conf = float(self.soup.find(name='span',
                                        attrs={'class': 'pdp-confidence-rating__copy'}).text.strip().split('%')[0])
        except AttributeError:
            conf = np.nan

        if len(values) == 1:
            values.append(np.nan)
            ranges.extend([np.nan, np.nan])
        elif not values:
            values.extend([np.nan, np.nan])
            ranges.extend([np.nan, np.nan, np.nan, np.nan])

        return {'buy': {'value': values[0], 'lower_bound': ranges[0], 'upper_bound': ranges[1]},
                'rent': {'value': values[1], 'lower_bound': ranges[2], 'upper_bound': ranges[3]},
                'confidence': conf}

    def value_change(self):
        period = [i.text for i in self.soup.find_all(name='span', attrs={'class': 'pdp-value-change__label'})]
        changes = [currency_to_num(i.text) for i in
                   self.soup.find_all(name='span', attrs={'class': 'pdp-value-change__value'})]
        diffs = [float(i.text.replace('%', '')) for i in
                 self.soup.find_all(name='span', attrs={'class': 'pdp-value-change__difference'})]

        df = pd.DataFrame(list(zip(period, changes, diffs)), columns=['period', 'value_change', 'perc_change'])
        df['value'] = self.property_value()['buy']['value'] / (1 + df.perc_change / 100)
        df['value'] = df.value.apply(myround)
        df = df[['period', 'value', 'value_change', 'perc_change']]

        return df

    def sales_history(self, dataframe=False):
        # historical listings available at https://www.zoopla.co.uk/property-history/{listing_id}
        history = {
            'date': [i.text for i in self.soup.find_all(name='span', attrs={'class': 'pdp-history__date'})],
            'status': [i.text for i in self.soup.find_all(name='span', attrs={'class': 'pdp-history__status'})],
            'price': [currency_to_num(i.text.replace('View listing', '')) for i in
                      self.soup.find_all(name='span', attrs={'class': 'pdp-history__price'})],
            'listing_id': []
        }

        for listing in self.soup.find_all(name='span', attrs={'class': 'pdp-history__price'}):
            try:
                history['listing_id'].append(listing.a['href'].split('/')[-1])
            except TypeError:
                history['listing_id'].append(np.nan)

        return pd.DataFrame(history) if dataframe else history

    def all_data(self, dataframe=True):

        data = self.details()
        data['address'] = str(self).split('Property details for ')[-1].split(' - Zoopla')[0]
        data['id'] = self.listing_id
        data['geolocation'] = self.location()
        data['for_sale_id'] = self.for_sale()
        data['property_value'] = self.property_value()
        data['value_change'] = self.value_change().to_dict()
        data['sales_history'] = self.sales_history()
        data['date_generated'] = datetime.now()

        return pd.DataFrame.from_dict(data, orient='index').T if dataframe else data
