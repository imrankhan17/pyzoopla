from httmock import all_requests, HTTMock, response
import pytest

from pyzoopla.prices import PricesSearch


def test_simple_prices_search():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/w1.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = PricesSearch('w1')

    assert str(results) == 'https://www.zoopla.co.uk/house-prices/w1/'
    assert results.location == 'w1'
    assert results.assumed_search_location == 'W1'
    assert results.total_properties == 18057
    assert results.total_pages == 452
    assert results.num_months is None
    assert results.property_type_code is None
    assert results.market_activity() == {'period': 20, 'property_type': 'all', 'average_price': 815521,
                                         'num_sales': 11192, 'average_value': 2041815, 'value_change': 1594930}
    assert results.market_activity(period=1) == {'period': 1, 'property_type': 'all', 'average_price': 2101974,
                                                 'num_sales': 243, 'average_value': 2041815, 'value_change': 57639}
    assert results.market_activity(period=5, property_type='terraced') == {'period': 5, 'property_type': 'terraced',
                                                                           'average_price': 4113439, 'num_sales': 132,
                                                                           'average_value': 4201518,
                                                                           'value_change': 765831}
    assert results.all_properties(page_limit=1) == ['24984791', '24984824', '24984827', '32015918', '31224282',
                                                    '31966815', '24984831', '24984833', '29168144', '24984819',
                                                    '32352479', '24984792', '29467841', '28263418', '32667778',
                                                    '32441152', '28833087', '24984784', '24984785', '24984786',
                                                    '24984787', '24984768', '24984769', '29023006', '31165661',
                                                    '24984645', '24984817', '24984832', '31964512', '29876454',
                                                    '29019891', '31464359', '32622368', '32695776', '24984834',
                                                    '29061498', '29876455', '31299781', '31299782', '31299783']


def test_complex_prices_search():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/e1.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = PricesSearch('e1', num_months=3, property_type_code='F')

    assert str(results) == 'https://www.zoopla.co.uk/house-prices/e1/?num_months=3&property_type_code=F'
    assert results.location == 'e1'
    assert results.assumed_search_location == 'E1'
    assert results.total_properties == 38
    assert results.total_pages == 1
    assert results.num_months == 3
    assert results.property_type_code == 'F'
    assert results.market_activity() == {'period': 20, 'property_type': 'all', 'average_price': 326240,
                                         'num_sales': 21206, 'average_value': 595808, 'value_change': 458353}
    assert results.market_activity(period=1) == {'period': 1, 'property_type': 'all', 'average_price': 585793,
                                                 'num_sales': 349, 'average_value': 595808, 'value_change': 20715}
    assert results.market_activity(period=5, property_type='terraced') == {'period': 5, 'property_type': 'terraced',
                                                                           'average_price': 861817, 'num_sales': 248,
                                                                           'average_value': 792981,
                                                                           'value_change': 224826}
    with pytest.raises(ValueError):
        results.market_activity(period=2)
    with pytest.raises(ValueError):
        results.market_activity(property_type='bungalow')
    assert results.all_properties(page_limit=1) == ['29594665', '7605668', '7605776', '7608535', '29503014', '7627919',
                                                    '30904195', '7609811', '30973201', '7607566', '7620679', '7625359',
                                                    '7614326', '7626841', '7604715', '7619868', '7629406', '7622162',
                                                    '7618631', '7622942', '7605936', '7631711', '7635734', '7635298',
                                                    '7632047', '7630842', '7633108', '7630918', '7634609', '7631034',
                                                    '7634653', '7631426', '7629831', '7632658', '7635546', '7631329',
                                                    '7635637', '7633019']
