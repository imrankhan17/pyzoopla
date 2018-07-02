import logging
import pymysql
import requests
import sys
import time

from pyzoopla.for_sale import ForSaleSearch
from pyzoopla.listing import PropertyListing
from pyzoopla.prices import PricesSearch
from pyzoopla.properties import PropertyDetails
from pyzoopla.utils import insert_into_db

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(funcName)s:%(lineno)d %(levelname)s - %(msg)s')


class BaseScraper:
    def __init__(self, location):
        self.location = location

    def save_data(self, database=None, port=None, user=None, password=None):
        """Output data to sql database."""
        raise NotImplementedError


class PropertyScraper(BaseScraper):

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

    def _get_property_ids(self, page_start=None, page_end=None):
        props, location, n_pages = self.search_prices()
        logging.info('About to scrape {} pages of properties for location {}.'.format(n_pages, location))
        return props.all_properties(page_start, page_end)

    def save_data(self, database=None, port=None, user=None, password=None):

        db_conn = pymysql.connect(host=database, port=port, user=user, password=password,
                                  cursorclass=pymysql.cursors.DictCursor)
        logging.info('Connected to database host: {}'.format(database))

        for prop_id in self._get_property_ids():

            try:
                logging.info('Scraping details for property ID: {}'.format(prop_id))
                prop = PropertyDetails(prop_id)
                insert_into_db(db_conn=db_conn, data=prop.all_data(dataframe=False), schema='zdb',
                               table='property_details')

                listing_id = prop.for_sale()
                if listing_id:
                    logging.info('Scraping details for property listing ID: {}'.format(listing_id))
                    listing = PropertyListing(listing_id)
                    insert_into_db(db_conn=db_conn, data=listing.details(dataframe=False), schema='zdb',
                                   table='listings_description')

            except AttributeError as err:
                logging.warning('Could not scrape property ID {}: {}'.format(prop_id, err))
                continue

            except requests.ConnectionError as err:
                logging.warning('Requests connection error occurred for property ID {}: {}'.format(prop_id, err))
                time.sleep(3)

        db_conn.close()
        logging.info('Finished scraping property details for location {}.'.format(self.location))


class SearchResultsScraper(BaseScraper):

    def save_data(self, database=None, port=None, user=None, password=None):

        db_conn = pymysql.connect(host=database, port=port, user=user, password=password, charset='utf8',
                                  cursorclass=pymysql.cursors.DictCursor)
        logging.info('Connected to database host: {}'.format(database))

        search = ForSaleSearch(self.location, distance=10)
        logging.info('Found {} properties in {} pages for location {}.'.format(search.total_properties,
                                                                               search.total_pages,
                                                                               search.assumed_search_location))

        for page in range(1, search.total_pages + 1):
            df = search.all_listings_page(page)
            for row in df.to_dict(orient='index').values():
                try:
                    logging.info('Scraping details for listing ID: {}'.format(row['listing_id']))
                    insert_into_db(db_conn=db_conn, data=row, schema='zdb', table='for_sale_listings')
                except AttributeError as err:
                    logging.info('Could not scrape listing ID {}: {}'.format(row['listing_id'], err))
                    continue

        db_conn.close()
        logging.info('Finished scraping listing details for location {}.'.format(search.assumed_search_location))
