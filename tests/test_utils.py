from bs4 import BeautifulSoup
import pytest

from tests.test_utils_data import *
from pyzoopla.utils import *


@pytest.fixture(scope='module')
def station_html():
    return [BeautifulSoup(html1, 'lxml'), BeautifulSoup(html2, 'lxml')]


def test_currency_to_num():
    assert currency_to_num('£100,000') == 100000
    assert currency_to_num('£100,000,000') == 100000000
    assert currency_to_num('100,000,000') == 100000000
    assert currency_to_num('£100') == 100
    assert currency_to_num('100') == 100
    assert currency_to_num(' \n £100,000 \n ') == 100000
    assert currency_to_num('£100.30', data_type=float) == 100.3
    assert currency_to_num('£100.30', data_type=int) == '100.30'
    assert currency_to_num(' £1,123,456.99\n pcm ', data_type=float) == 1123456.99


def test_myround():
    assert myround(110380, base=50) == 110400
    assert myround(110375, base=50) == 110400
    assert myround(110374, base=50) == 110350
    assert myround(110374.99, base=50) == 110350
    assert myround(110375.0, base=50) == 110400
    assert myround(10, base=10) == 10
    assert myround(0, base=10) == 0
    assert myround(0, base=100) == 0
    assert myround(210, base=10) == 210
    assert myround(215, base=10) == 220
    assert myround(214, base=10) == 210
    assert myround(214.99, base=10) == 210


@pytest.mark.parametrize('html,expected,data_type', [
    ('<span class="price-modifier">Guide price</span>', 'Guide price', str),
    ('<span class="num-icon num-beds" title="3 bedrooms"><span class="interface"></span>3</span>', 3, int),
    ('<span class="num-icon num-baths" title="1 bathroom"><span class="interface"></span>1</span>', 1, int),
    ('<span class="num-icon num-reception" title="2 reception rooms"><span class="interface"></span>2</span>', 2, int),
    ('<span class="num-icon num-beds" title="3 bedrooms"></span>', '', str)
])
def test_text_or_none(html, expected, data_type):
    assert text_or_none(soup=BeautifulSoup(html, 'lxml'), data_type=data_type) == expected


def test_to_datetime():
    assert to_datetime('1st Jun 2010') == datetime(2010, 6, 1, 0, 0)
    assert to_datetime('2nd Apr 2010') == datetime(2010, 4, 2, 0, 0)
    assert to_datetime('3rd Mar 2010') == datetime(2010, 3, 3, 0, 0)
    assert to_datetime('4th Feb 2009') == datetime(2009, 2, 4, 0, 0)
    assert to_datetime('19th Jan 2010') == datetime(2010, 1, 19, 0, 0)
    assert to_datetime('21st May 2012') == datetime(2012, 5, 21, 0, 0)


def test_get_station_name():
    data = station_html()
    assert get_station_name(soup=data, station_num=0) == 'London Bridge'
    assert get_station_name(soup=data, station_num=1) == 'Borough'


def test_dist_to_num():
    data = station_html()
    assert dist_to_num(data[0]) == 0.4
    assert dist_to_num(data[1]) == 1.2


def test_text_inbetween():
    string = 'The quick brown fox jumps over the lazy dog'
    assert text_inbetween(text=string, left='brown ', right=' over') == 'fox jumps'
    assert text_inbetween(text=string, left='brown', right='over') == ' fox jumps '
    assert text_inbetween(text=string, left='T', right='k') == 'he quic'
    assert text_inbetween(text=string, left='brown', right='fox') == ' '
