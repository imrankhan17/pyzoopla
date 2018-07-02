import argparse
import sys

from .scrape import ForSaleScraper, PropertyScraper, ToRentScraper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', '-l', dest='loc', type=str, required=True, help='Name of location e.g. postcode')
    parser.add_argument('--database', '-d', dest='database', help='Name of database endpoint')
    parser.add_argument('--port', '-o', dest='port', default=3306, help='Database port number')
    parser.add_argument('--user', '-u', dest='user', help='Database username')
    parser.add_argument('--password', '-p', dest='password', help='Database password')
    parser.add_argument('--test', '-t', dest='test', action='store_true', help='Get no. of properties for location')
    parser.add_argument('--property', '-r', dest='property', action='store_true', help='Scrape property results')
    parser.add_argument('--sale', '-s', dest='sale', action='store_true', help='Scrape for sale search results')
    parser.add_argument('--rent', '-n', dest='rent', action='store_true', help='Scrape to rent search results')
    args = parser.parse_args()

    if args.test:
        properties = PropertyScraper(location=args.loc)
        _ = properties.search_prices()

        for_sale_results = ForSaleScraper(location=args.loc)
        _ = for_sale_results.search_prices()

        to_rent_results = ToRentScraper(location=args.loc)
        _ = to_rent_results.search_prices()

        sys.exit()

    if args.property:
        properties = PropertyScraper(args.loc)
        properties.save_data(database=args.database, port=args.port, user=args.user, password=args.password)

    if args.sale:
        search = ForSaleScraper(args.loc)
        search.save_data(database=args.database, port=args.port, user=args.user, password=args.password)

    if args.rent:
        search = ToRentScraper(args.loc)
        search.save_data(database=args.database, port=args.port, user=args.user, password=args.password)


if __name__ == '__main__':
    main()
