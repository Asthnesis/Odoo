{
    'name': 'Montana Mall customizations',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Changes to Properties module',
    'description': """
    All montana mall customizations: Field definitions, additions and changes.
    - Link for customer and unit
    - location field for units
    - Is Available filter for free units
    - Computation for rental end date
    - Other Info fields: for if lease is picked, steel door and shutter door 
    -----------------------------------------------------------------------
        - Automatic capitalization of the customer name.
        - Title Case for product name.
        - Email validation.
        - Phone number must be 10 digits and numerical.
        - Tax ID format validation: A123456789B.
    - 
    """,
    'author': 'Edward R, James Oginga',
    'website': 'https://softiqtechnologies.co.ke',
    'license': 'AGPL-3',
    'depends': ['base','analytic','sale', 'sale_subscription','account','web'],  
    #  'assets': {
    #     'web.assets_backend': [
    #         'si_montana/static/src/js/sale_order_confirm_dialogue.js',
    #     ],
    # },

    'data': [
        'views/sale_order.xml',
        'views/rental_contract_view.xml',
        'data/compute_customers_cron.xml',
        'views/account_analytic_account_views.xml',
        'views/res_partner_views.xml',
        'views/account_payment_register.xml',
        'views/account_move.xml'
    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}
