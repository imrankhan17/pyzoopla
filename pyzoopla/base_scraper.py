import logging
import pymysql
import sys

from pyzoopla.utils import insert_into_db

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(funcName)s:%(lineno)d %(levelname)s - %(msg)s')


class BaseScraper:
    def __init__(self, location):
        self.location = location

    def search_prices(self):
        """Return search results object."""
        raise NotImplementedError

    def save_data(self, database=None, port=None, user=None, password=None):
        """Output data to sql database."""
        raise NotImplementedError


class BasePurchaseScraper:
    def __init__(self, location, scraper_object):
        self.location = location
        self.scraper_object = scraper_object

    def search_prices(self):
        results = self.scraper_object(location=self.location, distance=10)

        try:
            _ = results.assumed_search_location
        except AttributeError:
            logging.critical('No location named \'{}\''.format(self.location))
            sys.exit()

        logging.info('Found {:,} properties {} in {} pages for location {} with radius {} miles.'.format(
            results.total_properties, results.slug.replace('-', ' '), results.total_pages,
            results.assumed_search_location, results.distance))

        if results.total_properties > 10000:
            logging.warning('A maximum of 10,000 properties can be scraped for this location.')

        return results, results.assumed_search_location, results.total_pages

    def save_data(self, database=None, port=None, user=None, password=None):

        db_conn = pymysql.connect(host=database, port=port, user=user, password=password, charset='utf8',
                                  cursorclass=pymysql.cursors.DictCursor)
        logging.info('Connected to database host: {}'.format(database))

        results, search_location, total_pages = self.search_prices()

        for page in range(1, total_pages + 1):
            df = results.all_listings_page(page)
            for row in df.to_dict(orient='index').values():
                try:
                    logging.info('Scraping details for listing ID: {}'.format(row['listing_id']))
                    insert_into_db(db_conn=db_conn, data=row, schema='zdb',
                                   table='{}_listings'.format(results.slug.replace('-', '_')))
                except AttributeError as err:
                    logging.info('Could not scrape listing ID {}: {}'.format(row['listing_id'], err))
                    continue

        db_conn.close()
        logging.info('Finished scraping listing details for location {}.'.format(search_location))
