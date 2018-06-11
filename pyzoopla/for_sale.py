import requests

from pyzoopla.base import BasePurchaseSearch


class ForSaleSearch(BasePurchaseSearch):
    """
    Search for properties for sale from https://www.zoopla.co.uk/for-sale/property/{location}

    distance: {0, 0.25, 0.5, 1, 3, 5, 10, 15, 20, 30, 40}
    property_type: {property, houses, flats, farms-land}
    results_sort: {newest_listings, highest_price, lowest_price, most_reduced, most_popular}
    """

    slug = 'for-sale'

    def __init__(self, location, page_size=100, distance=None, min_price=None, max_price=None, min_beds=None,
                 max_beds=None, property_type='property', added=None, results_sort=None, include_sold=True,
                 has_parking_garage=None, has_garden=None, has_fireplace=None, has_wood_floors=None,
                 has_balcony_terrace=None, is_rural_secluded=None, has_porter_security=None, chain_free=False,
                 reduced_price_only=False, new_build=None, is_shared_ownership=False, is_auction=False,
                 is_retirement_home=False, buyer_incentive=None, keywords=None):
        self.distance = distance
        self.min_price = min_price
        self.max_price = max_price
        self.property_type = property_type
        self.min_beds = min_beds
        self.max_beds = max_beds
        self.added = added
        self.results_sort = results_sort
        self.include_sold = include_sold
        self.has_parking_garage = 'has_parking_garage' if has_parking_garage else None
        self.has_garden = 'has_garden' if has_garden else None
        self.has_fireplace = 'has_fireplace' if has_fireplace else None
        self.has_wood_floors = 'has_wood_floors' if has_wood_floors else None
        self.has_balcony_terrace = 'has_balcony_terrace' if has_balcony_terrace else None
        self.is_rural_secluded = 'is_rural_secluded' if is_rural_secluded else None
        self.has_porter_security = 'has_porter_security' if has_porter_security else None
        self.chain_free = str(chain_free).lower() if chain_free else None
        self.reduced_price_only = str(reduced_price_only).lower() if reduced_price_only else None
        self.new_build = new_build
        self.is_shared_ownership = str(is_shared_ownership).lower() if is_shared_ownership else None
        self.is_auction = str(is_auction).lower() if is_auction else None
        self.is_retirement_home = str(is_retirement_home).lower() if is_retirement_home else None
        self.buyer_incentive = 'help_to_buy' if buyer_incentive else None
        self.keywords = '"{}"'.format(keywords) if keywords else None
        super(ForSaleSearch, self).__init__(location, page_size)

    def _get_html(self, page_no=1):

        if self.added == 1:
            added = '24_hours'
        elif self.added:
            added = '{}_days'.format(self.added)
        else:
            added = None

        new_homes = None
        if self.new_build is None:
            pass
        elif self.new_build:
            self.slug = 'new-homes'
        else:
            new_homes = 'exclude'

        payload = {'radius': self.distance, 'price_min': self.min_price, 'price_max': self.max_price,
                   'beds_min': self.min_beds, 'beds_max': self.max_beds, 'added': added,
                   'results_sort': self.results_sort, 'include_sold': str(self.include_sold).lower(),
                   'page_size': self.page_size, 'pn': page_no,
                   'feature': [self.has_parking_garage, self.has_garden, self.has_fireplace, self.has_wood_floors,
                               self.has_balcony_terrace, self.is_rural_secluded, self.has_porter_security],
                   'chain_free': self.chain_free, 'reduced_price_only': self.reduced_price_only,
                   'new_homes': new_homes, 'is_shared_ownership': self.is_shared_ownership,
                   'is_auction': self.is_auction, 'is_retirement_home': self.is_retirement_home,
                   'buyer_incentive': self.buyer_incentive, 'keywords': self.keywords}
        url = 'https://www.zoopla.co.uk/{}/{}/{}/'.format(self.slug, self.property_type, self.location)

        return requests.get(url, params=payload)
