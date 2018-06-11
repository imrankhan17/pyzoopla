from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests

from pyzoopla.utils import currency_to_num, dist_to_num, get_station_name, text_or_none, to_datetime


class Base:
    """
    Base class which holds common methods for all classes in this package.
    """

    def __init__(self):
        self.html = self._get_html()
        self.soup = self._get_soup()

    def __repr__(self):
        """Default string representation of all package objects is its URL."""
        return self.html.url

    def __str__(self):
        return self.__repr__()

    def _get_html(self, page_no=None):
        """Makes request to website after constructing the relevant URL."""
        raise NotImplementedError

    def _get_soup(self, page_no=1):
        """Creates soup object from html."""
        return BeautifulSoup(self._get_html(page_no).text, 'lxml')

    def save(self, file_location):
        """Writes raw html to file."""
        with open(file_location, mode='wb') as file:
            file.write(self.html.content)


class BaseProperty(Base):
    """
    Base class for Zoopla pages containing the details of a single property.
    """

    def __init__(self, listing_id, slug):
        self.listing_id = listing_id
        self.slug = slug
        super(BaseProperty, self).__init__()

    def _get_html(self, page_no=None):
        payload = {'pn': page_no}
        url = 'https://ww2.zoopla.co.uk/{}/{}'.format(self.slug, self.listing_id)
        return requests.get(url, params=payload)


class BaseSearch(Base):
    """
    Base class for Zoopla pages containing the details of multiple properties i.e. search results.
    """

    def __init__(self, location, page_size=None):
        self.location = location
        self.page_size = page_size
        super(BaseSearch, self).__init__()

    @property
    def assumed_search_location(self):
        """Zoopla's assumed search string given user's input."""
        raise NotImplementedError

    @property
    def total_properties(self):
        """Total number of properties matching search criteria."""
        results = int(self.soup.find(name='span', attrs={'class': 'listing-results-utils-count'})
                      .text.split(' of ')[-1].replace(',', '').replace('+', ''))
        return results

    @property
    def total_pages(self):
        """Total number of pages of properties matching search criteria."""
        results = self.total_properties
        pages = (results // self.page_size) + 1 if results % self.page_size != 0 else results // self.page_size
        return pages


class BasePurchaseSearch(BaseSearch):
    """Base class for all property search results available to purchase (buy/rent)."""

    @property
    def assumed_search_location(self):
        return self.soup.find(name='span', attrs={'class': 'maps-area-name'}).b.text

    def _all_listings_page(self, page_no):
        """Search result details for a single page"""

        soup = self.soup if page_no == 1 else self._get_soup(page_no)
        listings = soup.find_all(name='li', attrs={'class': 'srp clearfix '}) + \
            soup.find_all(name='li', attrs={'class': 'srp clearfix premium-listing premium-listing--branded '})

        df = pd.DataFrame()
        df['listing_id'] = [i['data-listing-id'] for i in listings]
        df['listing_price'] = [currency_to_num(
            i.find(name='a',
                   attrs={'class': 'listing-results-price text-price'}).text.strip().split('\n')[0]) for i in listings]
        df['price_modifier'] = [text_or_none(i.find(name='span', attrs={'class': 'price-modifier'})) for i in listings]
        df['address'] = [i.find(name='a', attrs={'class': 'listing-results-address'}).text for i in listings]
        df['summary'] = [i.find(name='a', attrs={'style': 'text-decoration:underline;'}).text for i in listings]
        df['num_beds'] = [text_or_none(i.find(name='span', attrs={'class': 'num-icon num-beds'}), data_type=str)
                          for i in listings]
        df['num_baths'] = [text_or_none(i.find(name='span', attrs={'class': 'num-icon num-baths'}), data_type=str)
                           for i in listings]
        df['num_receptions'] = [text_or_none(
            i.find(name='span', attrs={'class': 'num-icon num-reception'}), data_type=str) for i in listings]
        df['description'] = [i.find(name='p').text.strip() for i in listings]
        df['listing_date'] = [to_datetime(
            i.find_all(name='small')[-1].text.split('Listed on \n')[1].split('\n')[0].strip()) for i in listings]
        df['estate_agent'] = [i.find(name='p', attrs={'class': 'top-half listing-results-marketed'}).span.text
                              for i in listings]
        df['station1'] = [get_station_name(i.find_all('li', attrs={'class': 'clearfix'}), 0) for i in listings]
        df['distance1'] = [dist_to_num(i.find_all('li', attrs={'class': 'clearfix'})[0]) for i in listings]
        df['station2'] = [get_station_name(i.find_all('li', attrs={'class': 'clearfix'}), 1) for i in listings]
        df['distance2'] = [dist_to_num(i.find_all('li', attrs={'class': 'clearfix'})[1]) for i in listings]
        df['date_generated'] = datetime.now()

        return df

    def all_listings(self, page_limit=None):
        """
        Summary of search results.
        :param page_limit: number of search result pages to consider.
        :return: Pandas dataframe.
        """

        page_limit = self.total_pages if not page_limit else page_limit
        data = [self._all_listings_page(page) for page in range(1, page_limit + 1)]
        return pd.concat(data).reset_index(drop=True)
