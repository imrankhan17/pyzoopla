import logging
import pymysql
import requests
import sys
import time

from pyzoopla.base_scraper import BasePurchaseScraper, BaseScraper
from pyzoopla.for_sale import ForSaleSearch
from pyzoopla.listing import PropertyListing
from pyzoopla.prices import PricesSearch
from pyzoopla.properties import PropertyDetails
from pyzoopla.to_rent import ToRentSearch
from pyzoopla.utils import insert_into_db

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(funcName)s:%(lineno)d %(levelname)s - %(msg)s')


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


class ForSaleScraper(BasePurchaseScraper):
    def __init__(self, location):
        super(ForSaleScraper, self).__init__(location, ForSaleSearch)


class ToRentScraper(BasePurchaseScraper):
    def __init__(self, location):
        super(ToRentScraper, self).__init__(location, ToRentSearch)
