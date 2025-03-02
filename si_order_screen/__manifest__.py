{
    'name': 'PoS Order Screen',
    'version': '1.0',
    'description': 'A screen that shows the orders to be printed on the kitchen receipt',
    'category': 'Point of Sale',
    'author':'Edward Rasto',
    'licence':'LGPL-3',
    'website': 'www.softiqtechnologies.co.ke',
    'depends': ['point_of_sale','si_actionpad_widget'],
    'data': [],
     'assets': {
            'point_of_sale._assets_pos': [
                'si_order_screen/static/src/js/order_screen.js',
                'si_order_screen/static/src/xml/order_screen.xml',
                'si_order_screen/static/src/xml/order_screen_receipt.xml',
            ]
    },

}
