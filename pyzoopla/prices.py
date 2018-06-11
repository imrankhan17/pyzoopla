from itertools import chain
import requests

from pyzoopla.base import BaseSearch


class PricesSearch(BaseSearch):
    """
    Get a list of property ID's from https://www.zoopla.co.uk/house-prices/{location}

    num_months: sales in the last {3, 6, 12, 60, 120, 240} months
    property_type_code: {D, S, T, F}
    """

    page_size = 40

    def __init__(self, location, num_months=None, property_type_code=None):
        self.num_months = num_months
        self.property_type_code = property_type_code
        super(PricesSearch, self).__init__(location, self.page_size)

    def _get_html(self, page_no=None):
        payload = {'num_months': self.num_months, 'property_type_code': self.property_type_code, 'pn': page_no}
        url = 'https://www.zoopla.co.uk/house-prices/{}/'.format(self.location)
        return requests.get(url, params=payload)

    @property
    def assumed_search_location(self):
        return self.soup.find(name='h1', attrs={'class': 'h-header'}).text.split('House prices in ')[-1]

    @staticmethod
    def _extract_ids(soup):
        return [address.a['href'].split('/')[-1] for address in
                soup.find_all(name='td', attrs={'class': 'browse-cell-address'})]

    def _get_ids_page(self, page_no):
        """
        Get list of property id's from a single page
        """
        soup = self._get_soup(page_no)
        return self._extract_ids(soup)

    def all_properties(self, page_limit=None):

        n_pages = page_limit if page_limit else self.total_pages

        if n_pages == 1:
            return self._extract_ids(self.soup)
        else:
            prop_id_list = [self._get_ids_page(page_no) for page_no in range(2, n_pages + 1)]
            return self._extract_ids(self.soup) + list(chain(*prop_id_list))

    def market_activity(self, period=20, property_type='all'):
        """
        Historical market activity for this location.

        :param period: last n years where n is measured in years,
                       options are {0.25, 0.5, 1, 5, 10, 20}
        :param property_type: options are {'all', 'detached', 'semi', 'terraced', 'flat'}
        :return: dictionary containing values for average price paid, no. of sales,
                 current average value and value change.
        """
        period_map = {0.25: 0, 0.5: 1, 1: 2, 5: 3, 10: 4, 20: 5}
        prop_type_map = {'all': 'data-value-all', 'detached': 'data-value-d', 'semi': 'data-value-s',
                         'terraced': 'data-value-t', 'flat': 'data-value-f'}

        if period not in period_map.keys():
            raise ValueError('period should be one of {}'.format(list(period_map.keys())))

        if property_type not in prop_type_map.keys():
            raise ValueError('property_type should be one of {}'.format(list(prop_type_map.keys())))

        summary = {'period': period, 'property_type': property_type}
        for stat in self.soup.find_all(name='span', attrs={'class': 'market-panel-stat-element-value'}):
            stat_name = stat['class'][1].split('stats-')[-1].replace('-', '_')
            summary[stat_name] = int(stat[prop_type_map[property_type]].split(',')[period_map[period]])

        return summary
