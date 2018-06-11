from httmock import all_requests, HTTMock, response
import pandas as pd
from pandas.util.testing import assert_frame_equal

from pyzoopla.for_sale import ForSaleSearch


def test_simple_search():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/london.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = ForSaleSearch(location='london')

    df_out = results.all_listings(page_limit=1).drop('date_generated', axis=1)
    df_expected = pd.read_csv('tests/test_data/london_expected.csv', dtype={'listing_id': 'str'},
                              parse_dates=['listing_date'], keep_default_na=False)

    assert_frame_equal(df_out, df_expected)
    assert str(results) == 'https://www.zoopla.co.uk/for-sale/property/london/?include_sold=true&page_size=100&pn=1'
    assert results.slug == 'for-sale'
    assert results.assumed_search_location == 'London'
    assert results.total_properties == 10000
    assert results.total_pages == 100
    assert results.distance is None
    assert results.added is None
    assert results.include_sold


def test_complex_search():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/sw7.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = ForSaleSearch(location='sw7', new_build=True, distance=10, min_price=300000, max_price=1000000,
                                min_beds=2, max_beds=4, has_parking_garage=True, added=7)

    df_out = results.all_listings(page_limit=1).drop(['date_generated'], axis=1)
    df_out.listing_price = df_out.listing_price.astype('str')
    df_expected = pd.read_csv('tests/test_data/sw7_expected.csv', dtype={'listing_id': 'str', 'num_beds': 'str'},
                              parse_dates=['listing_date'], keep_default_na=False)

    assert_frame_equal(df_out, df_expected)
    assert str(results) == 'https://www.zoopla.co.uk/new-homes/property/sw7/?radius=10&price_min=300000&' \
                           'price_max=1000000&beds_min=2&beds_max=4&added=7_days&include_sold=true&page_size=100&' \
                           'pn=1&feature=has_parking_garage'
    assert results.slug == 'new-homes'
    assert results.assumed_search_location == 'SW7'
    assert results.total_properties == 82
    assert results.total_pages == 1
    assert results.new_build
    assert results.distance == 10
    assert results.min_price == 300000
    assert results.max_price == 1000000
    assert results.min_beds == 2
    assert results.max_beds == 4
    assert results.has_parking_garage
    assert results.added == 7
    assert results.buyer_incentive is None
    assert results.has_balcony_terrace is None
