{
    'name': 'PoS Order Line Sequence',
    'version': '1.1',

    'summary': 'Sequence numbers in PoS order lines of Point of Sale',
    'description': """This module will help you to add sequence for order lines
                      in Point of sale.""",
    'author': 'Edward R',
    'company': 'SoftIQ Technologies',
    'website': "https://www.softiqtechnologies.co.ke",
    'license': 'AGPL-3',
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'web.assets_backend': [],
        'point_of_sale.assets': [
            'si_pos_orderline/static/src/js/orderline.js',
            'si_pos_orderline/static/src/xml/orderline.xml',        ],
    },
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
