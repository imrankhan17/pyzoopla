import argparse

from .scrape import PropertyScraper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', '-l', dest='loc', type=str, required=True, help='Name of location e.g. postcode')
    parser.add_argument('--test', '-t', dest='test', action='store_true', help='Get no. of properties for location')
    args = parser.parse_args()

    properties = PropertyScraper(args.loc)

    if args.test:
        _ = properties.search_prices()
    else:
        properties.save_data()


if __name__ == '__main__':
    main()
