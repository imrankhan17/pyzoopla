from httmock import all_requests, HTTMock, response
import pandas as pd
from pandas.util.testing import assert_frame_equal

from pyzoopla.to_rent import ToRentSearch


def test_simple_search():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/london_rent.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = ToRentSearch(location='london')

    df_out = results.all_listings(page_limit=1).drop('date_generated', axis=1)
    df_expected = pd.read_csv('tests/test_data/london_rent_expected.csv', dtype={'listing_id': 'str'},
                              parse_dates=['listing_date'], keep_default_na=False)

    assert_frame_equal(df_out, df_expected)
    assert str(results) == 'https://www.zoopla.co.uk/to-rent/property/london/?page_size=100&pn=1&' \
                           'price_frequency=per_month'
    assert results.slug == 'to-rent'
    assert results.assumed_search_location == 'London'
    assert results.total_properties == 10000
    assert results.total_pages == 100
    assert results.distance is None
    assert results.added is None


def test_complex_search():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/sw7_rent.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = ToRentSearch(location='sw7', available=3, distance=10, min_price=100, max_price=2000,
                               min_beds=2, max_beds=4, has_parking_garage=True, added=7)

    df_out = results.all_listings(page_limit=1).drop(['date_generated'], axis=1)
    df_out.listing_price = df_out.listing_price.astype('str')
    df_expected = pd.read_csv('tests/test_data/sw7_rent_expected.csv', dtype={'listing_id': 'str', 'num_beds': 'str'},
                              parse_dates=['listing_date'], keep_default_na=False)

    assert_frame_equal(df_out, df_expected)
    assert str(results) == 'https://www.zoopla.co.uk/to-rent/property/sw7/?radius=10&price_min=100&' \
                           'price_max=2000&beds_min=2&beds_max=4&added=7_days&page_size=100&pn=1&' \
                           'available_from=3months&price_frequency=per_month&feature=has_parking_garage'
    assert results.slug == 'to-rent'
    assert results.assumed_search_location == 'SW7'
    assert results.total_properties == 1021
    assert results.total_pages == 11
    assert results.distance == 10
    assert results.min_price == 100
    assert results.max_price == 2000
    assert results.min_beds == 2
    assert results.max_beds == 4
    assert results.has_parking_garage
    assert results.added == 7
    assert results.has_balcony_terrace is None
    assert results.furnished_state is None
