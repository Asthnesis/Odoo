{
    'name': 'Lock',
    'version': '1.0',
    'category': 'Properties',
    'summary': '',
    'description': """
    Allows addition and removal of meter numbers and their status from Properties and buildings
    """,
    'author': 'Edward R',
    'website': 'https://softiqtechnologies.co.ke',
    'license': 'AGPL-3',
    'depends': ['base','analytic', 'account','sale'],  
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/product_product_template.xml',
        'views/sale_order.xml',
        #'views/rental_contract.xml',
        
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
