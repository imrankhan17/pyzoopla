import argparse

from .scrape import PropertyScraper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', '-l', dest='loc', type=str, required=True, help='Name of location e.g. postcode')
    parser.add_argument('--database', '-d', dest='database', help='Name of database endpoint')
    parser.add_argument('--port', '-o', dest='port', default=3306, help='Database port number')
    parser.add_argument('--user', '-u', dest='user', help='Database username')
    parser.add_argument('--password', '-p', dest='password', help='Database password')
    parser.add_argument('--schema', '-s', dest='schema', help='Name of database schema')
    parser.add_argument('--table', '-b', dest='table', help='Name of database table')
    parser.add_argument('--test', '-t', dest='test', action='store_true', help='Get no. of properties for location')
    args = parser.parse_args()

    properties = PropertyScraper(args.loc)

    if args.test:
        _ = properties.search_prices()
    else:
        properties.save_data(database=args.database, port=args.port, user=args.user, password=args.password,
                             schema=args.schema, table=args.table)


if __name__ == '__main__':
    main()
