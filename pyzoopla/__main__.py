import argparse

from .scrape import PropertyScraper, SearchResultsScraper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', '-l', dest='loc', type=str, required=True, help='Name of location e.g. postcode')
    parser.add_argument('--database', '-d', dest='database', help='Name of database endpoint')
    parser.add_argument('--port', '-o', dest='port', default=3306, help='Database port number')
    parser.add_argument('--user', '-u', dest='user', help='Database username')
    parser.add_argument('--password', '-p', dest='password', help='Database password')
    parser.add_argument('--test', '-t', dest='test', action='store_true', help='Get no. of properties for location')
    parser.add_argument('--property', '-r', dest='property', action='store_true', help='Scrape property results')
    parser.add_argument('--search', '-s', dest='search', action='store_true', help='Scrape for sale search results')
    args = parser.parse_args()

    if args.test:
        properties = PropertyScraper(args.loc)
        _ = properties.search_prices()

    if args.property:
        properties = PropertyScraper(args.loc)
        properties.save_data(database=args.database, port=args.port, user=args.user, password=args.password)

    if args.search:
        search = SearchResultsScraper(args.loc)
        search.save_data(database=args.database, port=args.port, user=args.user, password=args.password)


if __name__ == '__main__':
    main()
