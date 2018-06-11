import requests

from pyzoopla.base import BasePurchaseSearch


class ToRentSearch(BasePurchaseSearch):
    """
    Search for properties to rent from https://www.zoopla.co.uk/to-rent/property/{location}

    distance: {0, 0.25, 0.5, 1, 3, 5, 10, 15, 20, 30, 40}
    property_type: {property, houses, flats, farms-land}
    results_sort: {newest_listings, highest_price, lowest_price, most_reduced, most_popular}
    price_frequency: {per_month, per_week}
    rental_term: {short}
    furnished_state: {furnished, part_furnished, unfurnished}
    """

    def __init__(self, location, page_size=100, slug='to-rent', added=None, available=None, distance=None,
                 include_rented=None, include_shared_accommodation=None, price_frequency='per_month', min_price=None,
                 max_price=None, min_beds=None, max_beds=None, results_sort=None, has_parking_garage=None,
                 has_garden=None, has_fireplace=None, has_wood_floors=None, has_balcony_terrace=None,
                 is_rural_secluded=None, has_porter_security=None, property_type='property', rental_term=None,
                 pets_allowed=None, bills_included=None, furnished_state=None, keywords=None):
        self.slug = slug
        self.added = added
        self.available = available
        self.distance = distance
        self.include_rented = str(include_rented).lower() if include_rented else None
        self.include_shared = str(include_shared_accommodation).lower() if include_shared_accommodation else None
        self.price_frequency = price_frequency
        self.min_price = min_price
        self.max_price = max_price
        self.min_beds = min_beds
        self.max_beds = max_beds
        self.results_sort = results_sort
        self.has_parking_garage = 'has_parking_garage' if has_parking_garage else None
        self.has_garden = 'has_garden' if has_garden else None
        self.has_fireplace = 'has_fireplace' if has_fireplace else None
        self.has_wood_floors = 'has_wood_floors' if has_wood_floors else None
        self.has_balcony_terrace = 'has_balcony_terrace' if has_balcony_terrace else None
        self.is_rural_secluded = 'is_rural_secluded' if is_rural_secluded else None
        self.has_porter_security = 'has_porter_security' if has_porter_security else None
        self.property_type = property_type
        self.rental_term = rental_term
        self.pets_allowed = str(pets_allowed).lower() if pets_allowed else None
        self.bills_included = str(bills_included).lower() if bills_included else None
        self.furnished_state = furnished_state
        self.keywords = '"{}"'.format(keywords) if keywords else None
        super(ToRentSearch, self).__init__(location, page_size)

    def _get_html(self, page_no=1):

        if self.added == 1:
            added = '24_hours'
        elif self.added:
            added = '{}_days'.format(self.added)
        else:
            added = None

        if self.available == 0:
            available = 'now'
        elif self.available:
            available = '{}months'.format(self.available)
        else:
            available = None

        payload = {'radius': self.distance, 'price_min': self.min_price, 'price_max': self.max_price,
                   'beds_min': self.min_beds, 'beds_max': self.max_beds, 'added': added,
                   'results_sort': self.results_sort, 'page_size': self.page_size, 'pn': page_no,
                   'include_rented': self.include_rented, 'include_shared_accommodation': self.include_shared,
                   'available_from': available, 'price_frequency': self.price_frequency,
                   'rental_term': self.rental_term, 'pets_allowed': self.pets_allowed,
                   'bills_included': self.bills_included, 'furnished_state': self.furnished_state,
                   'feature': [self.has_parking_garage, self.has_garden, self.has_fireplace, self.has_wood_floors,
                               self.has_balcony_terrace, self.is_rural_secluded, self.has_porter_security],
                   'keywords': self.keywords}
        url = 'https://www.zoopla.co.uk/{}/{}/{}/'.format(self.slug, self.property_type, self.location)

        return requests.get(url, params=payload)
