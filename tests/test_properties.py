from httmock import all_requests, HTTMock, response
import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

from pyzoopla.properties import PropertyDetails


def test_property_details_all_methods():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/property1.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = PropertyDetails(10647960)

    assert str(results) == 'Property details for 7 Anstey Brook Weston Turville Aylesbury HP22 5RT'
    assert repr(results) == 'https://ww2.zoopla.co.uk/property/10647960'
    assert results.listing_id == 10647960
    assert results.slug == 'property'
    assert results.details() == {'acorn_type': '8', 'activity': 'property_details', 'country_code': 'gb',
                                 'incode': '5RT', 'listing_id': '10647960', 'location': 'HP225RT', 'num_baths': '2',
                                 'num_beds': '4', 'outcode': 'HP22', 'page': '/property/details/', 'postal_area': 'HP',
                                 'price': '512922', 'price_estimate': '512922', 'price_last_sale': '510000',
                                 'price_temptme': 'null', 'property_type': 'semi_detached', 'rental_value': '1583',
                                 'section': 'home-values'}
    assert results.location() == {'is_approximate': False, 'latitude': 51.79233, 'longitude': -0.75069}
    assert not results.for_sale()
    assert results.property_value() == {'buy': {'value': 513000, 'lower_bound': 503000, 'upper_bound': 523000},
                                        'rent': {'value': 1600, 'lower_bound': 1400, 'upper_bound': 1800},
                                        'confidence': 99.5}
    assert_frame_equal(results.value_change(), pd.DataFrame([
        ['last sold (Oct 2017)', 509950, 3000, 0.6], ['1 month ago', 513500, 450, -0.1],
        ['3 months ago', 509950, 2850, 0.6], ['6 months ago', 510450, 2650, 0.5], ['1 year ago', 531050, 18200, -3.4],
        ['2 years ago', 496600, 16200, 3.3], ['3 years ago', 442250, 70850, 16.0],
        ['4 years ago', 412700, 100300, 24.3], ['5 years ago', 372300, 140600, 37.8]],
        columns=['period', 'value', 'value_change', 'perc_change']))
    assert results.sales_history(dataframe=False) == {
        'date': ['Oct 2017', 'Jul 2017', 'Mar 2014', 'Apr 2013', 'Mar 1997'],
        'listing_id': [np.nan, '44447984', np.nan, '28558762', np.nan],
        'price': [510000, 500000, 390000, 410000, 111500],
        'status': ['Sold', 'Listed for sale', 'Sold', 'Listed for sale', 'Sold']}


def test_property_details_for_sale():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/property2.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = PropertyDetails(32458972)

    assert results.for_sale() == '45395750'


def test_property_details_empty_data():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/property3.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = PropertyDetails(31866527)

    assert len(results.value_change()) == 0
    assert not results.for_sale()
    assert results.sales_history() == {'date': [], 'listing_id': [], 'price': [], 'status': []}
    assert results.property_value() == {'buy': {'lower_bound': np.nan, 'upper_bound': np.nan, 'value': np.nan},
                                        'confidence': np.nan,
                                        'rent': {'lower_bound': np.nan, 'upper_bound': np.nan, 'value': np.nan}}


def test_property_details_all_data():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/property4.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = PropertyDetails(10605934)

    df = results.all_data()
    assert df.drop('date_generated', axis=1).to_dict(orient='list') == {
        'acorn_type': ['19'],
        'activity': ['property_details'],
        'country_code': ['gb'],
        'incode': ['8DJ'],
        'listing_id': ['10605934'],
        'location': ['HP178DJ'],
        'num_baths': ['1'],
        'num_beds': ['2'],
        'outcode': ['HP17'],
        'page': ['/property/details/'],
        'postal_area': ['HP'],
        'price': ['329689'],
        'price_estimate': ['329689'],
        'price_last_sale': ['337000'],
        'price_temptme': ['null'],
        'property_type': ['terraced'],
        'rental_value': ['924'],
        'section': ['home-values'],
        'address': ['28 Anxey Way Haddenham Aylesbury HP17 8DJ'],
        'id': [10605934],
        'geolocation': [{'is_approximate': False, 'latitude': 51.772993, 'longitude': -0.933549}],
        'for_sale_id': [False],
        'property_value': [{'buy': {'value': 330000, 'lower_bound': 323000, 'upper_bound': 336000},
                            'rent': {'value': 900, 'lower_bound': 800, 'upper_bound': 1050},
                            'confidence': 99.5}],
        'value_change': [{'period': {0: 'last sold (Mar 2017)', 1: '1 month ago', 2: '3 months ago', 3: '6 months ago',
                                     4: '1 year ago', 5: '2 years ago', 6: '3 years ago', 7: '4 years ago',
                                     8: '5 years ago'},
                          'value': {0: 337100, 1: 330350, 2: 332000, 3: 337750, 4: 346250, 5: 325100, 6: 283250,
                                    7: 264000, 8: 243000},
                          'value_change': {0: 7000, 1: 450, 2: 2050, 3: 7850, 4: 16200, 5: 5000, 6: 46700, 7: 66000,
                                           8: 86900},
                          'perc_change': {0: -2.1, 1: -0.1, 2: -0.6, 3: -2.3, 4: -4.7, 5: 1.5, 6: 16.5, 7: 25.0,
                                          8: 35.8}}],
        'sales_history': [{'date': ['Mar 2017', 'Nov 2016', 'Feb 2012', 'Aug 2011', 'Feb 2005', 'May 1999'],
                           'status': ['Sold', 'Listed for sale', 'Sold', 'Listed for sale', 'Sold', 'Sold'],
                           'price': [337000, 345000, 220000, 225000, 178000, 83000],
                           'listing_id': [np.nan, '42187797', np.nan, '22249243', np.nan, np.nan]}]
    }
