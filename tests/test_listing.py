from httmock import all_requests, HTTMock, response

from pyzoopla.listing import PropertyHistoricalListing, PropertyListing


def test_listing_few_details():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/listing.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = PropertyListing(47902463)

    assert str(results) == 'https://ww2.zoopla.co.uk/for-sale/details/47902463'
    assert results.listing_id == 47902463
    assert results.slug == 'for-sale/details'
    assert results.details(dataframe=False) == {
        'listing_id': 47902463,
        'description': "\n                        A lovely three, three bathroom bedroom third floor Marylebone "
                       "apartment in a prestigious mansion block with lift and porter. Beautifully presented "
                       "throughout, comprising a master bedroom with en suite shower room, two further double "
                       "bedrooms, two further shower rooms, and a large semi open plan kitchen/reception room with "
                       "dining area. Further features bright and charming rooms, neutral décor and ample storage.You "
                       "may download, store and use the material for your own personal use and research. You may not "
                       "republish, retransmit, redistribute or otherwise make the material available to any party or "
                       "make the same available on any website, online service or bulletin board of your own or of "
                       "any other party or make the same available in hard copy or in any other media without the "
                       "website owner's express prior written consent. The website owner's copyright must remain on "
                       "all reproductions of material taken from this website.\n                    ",
        'main_features': ['3                bedrooms', '3                bathrooms', '1                reception room',
                          'floor area1,163 sq. ft'],
        'more_features': [],
        'price_history': {'date': ['7th Jun 2018'],
                          'price': [2295000],
                          'detail': ['First listed']}
    }


def test_listing_more_details():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/listing2.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = PropertyListing(38834402)

    assert str(results) == 'https://ww2.zoopla.co.uk/for-sale/details/38834402'
    assert results.listing_id == 38834402
    assert results.slug == 'for-sale/details'
    assert results.details(dataframe=True).to_dict() == {
        'listing_id': {0: 38834402},
        'description': {0: '\n                        Set within a superb portered building just south of Oxford '
                           'Street, this fantastic two bedroom, two bathroom apartment offers beautifully presented '
                           'living space with classic décor.A wealth of exclusive boutiques and eateries can be found '
                           'throughout Mayfair, Oxford Street and Regent Street offer world class shops and department'
                           ' stores. Hyde Park is also moments away.\n                    '},
        'main_features': {0: ['2                bedrooms']},
        'more_features': {0: ['Secure entry and lift access to the second floor',
                              'Generous reception room with lots of natural light',
                              'Separate modern kitchen with ample storage space',
                              'Master bedroom with fitted wardrobe and en suite',
                              'Good-sized second bedroom with fitted wardrobe',
                              'Well presented shower room',
                              'Large entrance hall with storage cupboards']},
        'price_history': {0: {'date': ['18th Apr 2018', '22nd Dec 2015', '19th Feb 2015', '29th Oct 2014'],
                              'price': [2300000, 2599000, 2800000, 3000000],
                              'detail': ['Price reduced by £299,000', 'Price reduced by £201,000',
                                         'Price reduced by £200,000', 'First listed']}}
    }


def test_historical_listing_details():

    @all_requests
    def zoopla_mock(url, request):
        content = open('tests/test_data/historical.txt', 'r').read()
        return response(content=content, request=request)

    with HTTMock(zoopla_mock):
        results = PropertyHistoricalListing(37047136)

    assert str(results) == 'Property history of 108 Shoreditch High Street, London E1 6JN, \n29th May 2015'
    assert results.listing_id == 37047136
    assert results.slug == 'property-history'
    assert results.details(dataframe=False) == {
        'listing_id': 37047136,
        'description': ". . .                 This wonderfully bright and spacious one bedroom apartment occupies the "
                       "third floor of a sympathetically restored Victorian building.Offering approximately 734 sq. "
                       "Ft. Of space this larger than average one bedroom boasts a stylish finish in the form of "
                       "exposed brick work, wood flooring, double glazed sash windows and a bespoke kitchen with "
                       "Siemens ovens and induction hob.Comprising an open plan dual aspect kitchen and living space, "
                       "generous double bedroom with fitted wardrobes and a high quality bathroom with a large "
                       "walk-in shower and storage spaces.Enjoying a fantastic locationin the heart of vibrant "
                       "Shoreditch, home to an increasing number of boutique clothing shops, the Ace Hotel and an "
                       "array of excellent bars and restaurants. Fashionable Brick Lane and Columbia Road are also "
                       "close by.A number of transport links serve the property including Shoreditch High Street "
                       "(Overground) just a stone's throw away, Old Street Station (National Rail, Northern Line) and "
                       "the major hub of Liverpool Street.Offered with no onward chain.. .             . . . . ",
        'features': '. . 734 sq. Ft. One bedroom apartment. Victorian conversion. High specification finish. Exposed '
                    'brick/sash windows/wood flooring. Central Shoreditch location. . . . '
    }
