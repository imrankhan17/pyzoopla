import logging
import sys

from pyzoopla.prices import PricesSearch
from pyzoopla.properties import PropertyDetails
from pyzoopla.utils import output_data

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s %(funcName)s:%(lineno)d - %(msg)s')


class PropertyScraper:

    def __init__(self, location):
        self.location = location

    def search_prices(self):
        search = PricesSearch(location=self.location)

        try:
            _ = search.assumed_search_location
        except AttributeError:
            logging.critical('No location named \'%s\'', self.location)
            sys.exit()

        logging.info('Found %s properties in location: %s.', search.total_properties, search.assumed_search_location)

        if search.total_properties > 100000:
            logging.warning('There are more than 100,000 properties for this location.')

        return search

    def _get_property_ids(self, page_limit=None):
        props = self.search_prices()
        n_pages = page_limit if page_limit else props.total_pages
        logging.info('About to scrape %s pages of properties.', n_pages)
        return props.all_properties(page_limit=page_limit)

    def save_data(self):
        """Output csv data to disk."""
        for prop_id in self._get_property_ids():
            prop = PropertyDetails(prop_id)
            logging.info('Scraping details for property: %s', prop.listing_id)
            output_data(prop.all_data(), self.location)

        logging.info('Finished scraping property details for location: %s.  Data has been saved to: %s',
                     self.search_prices().assumed_search_location, 'data/data_{}.csv'.format(self.location).lower())
