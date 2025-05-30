{
    'name': 'Patch for Meters model',
    'version': '1.0',
    'category': 'Properties',
    'summary': 'Meters Model',
    'description': """
    Allows addition and removal of meter numbers and their status from Properties and buildings
    """,
    'author': 'Edward R',
    'website': 'https://softiqtechnologies.co.ke',
    'license': 'AGPL-3',
    'depends': ['base','analytic', 'account'],  
    'data': [
        'views/si_meters.xml',
        'views/account_analytic_account.xml',
        'security/ir.model.access.csv',
    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}
