import pandas as pd

from pyzoopla.base import BaseProperty
from pyzoopla.utils import currency_to_num, text_inbetween, text_or_none


class PropertyListing(BaseProperty):
    """
    For sale listings available at https://ww2.zoopla.co.uk/for-sale/details/{listing_id}
    """

    def __init__(self, listing_id):
        super(PropertyListing, self).__init__(listing_id, slug='for-sale/details')

    def _price_history(self):
        dates = [i.text for i in self.soup.find_all(name='span', attrs={'class': 'dp-price-history__item-date'})]
        prices = [currency_to_num(i.text) for i in
                  self.soup.find_all(name='span', attrs={'class': 'dp-price-history__item-price'})]
        details = [i.text.strip() for i in
                   self.soup.find_all(name='span', attrs={'class': 'dp-price-history__item-detail'})]

        return {'date': dates, 'price': prices, 'detail': details}

    def details(self, dataframe=True):
        description = text_or_none(self.soup.find(name='div', attrs={'class': 'dp-description__text'}))
        main = [icon.text.strip() for icon in
                self.soup.find_all(name='li', attrs={'class': 'ui-list-icons__item'})]
        features = text_or_none(self.soup.find(name='ul',
                                               attrs={'class': 'dp-features__list ui-list-bullets'})).split('\n')[1:-1]
        price_history = self._price_history()
        data = {'listing_id': self.listing_id, 'description': description, 'main_features': main,
                'more_features': features, 'price_history': price_history}

        return pd.DataFrame.from_dict(data, orient='index').T if dataframe else data


class PropertyHistoricalListing(BaseProperty):
    """
    Historical listings available at https://www.zoopla.co.uk/property-history/{listing_id}
    """

    def __init__(self, listing_id):
        super(PropertyHistoricalListing, self).__init__(listing_id, slug='property-history')

    def __str__(self):
        # Address of the property and listing date
        return self.soup.find(name='h1', attrs={'class': 'bottom-half'}).text.strip()

    def details(self, dataframe=True):
        string = self.soup.find(name='div', attrs={'id': 'historic-listing-content'}).text
        features = text_inbetween(string.replace('\n', '. '), 'Property features', 'Property description')
        description = text_inbetween(string.replace('\n', '. '), 'Property description', 'Previously marketed by')
        data = {'listing_id': self.listing_id, 'description': description, 'features': features}

        return pd.DataFrame.from_dict(data, orient='index').T if dataframe else data
