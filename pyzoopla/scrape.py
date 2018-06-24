import logging
import pymysql
import sys

from pyzoopla.prices import PricesSearch
from pyzoopla.properties import PropertyDetails
from pyzoopla.utils import insert_into_db

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
            logging.warning('A maximum of 100,000 properties can be scraped for this location.')

        return search, search.assumed_search_location, search.total_pages

    def _get_property_ids(self):
        props, location, n_pages = self.search_prices()
        logging.info('About to scrape {} pages of properties for location {}.'.format(n_pages, location))
        return props.all_properties()

    def save_data(self, database=None, port=None, user=None, password=None, schema=None, table=None):
        """Output csv data to disk."""

        db_conn = pymysql.connect(host=database, port=port, user=user, password=password,
                                  cursorclass=pymysql.cursors.DictCursor)
        cur = db_conn.cursor()
        logging.info('Connected to database host: {}'.format(database))

        for prop_id in self._get_property_ids():
            logging.info('Scraping details for property ID: {}'.format(prop_id))
            prop = PropertyDetails(prop_id)
            insert_into_db(db_conn=db_conn, cur=cur, data=prop.all_data(dataframe=False), schema=schema, table=table)

        db_conn.close()
        logging.info('Finished scraping property details')
