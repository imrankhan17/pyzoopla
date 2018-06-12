import logging
import sys

from pyzoopla.prices import PricesSearch
from pyzoopla.properties import PropertyDetails
from pyzoopla.utils import output_data

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(funcName)s:%(lineno)d %(levelname)s - %(msg)s')


class PropertyScraper:

    def __init__(self, location):
        self.location = location

    def search_prices(self):
        search = PricesSearch(location=self.location)

        try:
            _ = search.assumed_search_location
        except AttributeError:
            logging.critical('No location named \'{}\''.format(self.location))
            sys.exit()

        logging.info('Found {:,} properties in location: {}.'.format(search.total_properties,
                                                                     search.assumed_search_location))

        if search.total_properties > 100000:
            logging.warning('A maximum of 100,000 properties will be scraped for this location.')

        return search

    def _get_property_ids(self, page_limit=None):
        props = self.search_prices()
        n_pages = page_limit if page_limit else props.total_pages
        logging.info('About to scrape {} pages of properties.'.format(n_pages))
        return props.all_properties(page_limit=page_limit)

    def save_data(self, output_dir='data'):
        """Output csv data to disk."""
        for prop_id in self._get_property_ids():
            prop = PropertyDetails(prop_id)
            logging.info('Scraping details for property ID: {}'.format(prop.listing_id))
            output_data(df=prop.all_data(), output_dir=output_dir, location=self.location)

        logging.info('Finished scraping property details.  Data has been saved to: {}'
                     .format('{}/data_{}.csv'.format(output_dir, self.location).lower()))
