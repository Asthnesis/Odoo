{
    'name': 'Lock/Unlock',
    'version': '1.0',
    'category': 'Properties',
    'summary': 'Lock/Unlock fields in account.analytic account especially in the properties module',
    'description': """
    Allows addition and removal of meter numbers and their status from Properties and buildings
    """,
    'author': 'Edward R',
    'website': 'https://softiqtechnologies.co.ke',
    'license': 'AGPL-3',
    'depends': ['base','analytic', 'account','sale'],  
    'data': [
        #'security/security.xml',
        #'security/ir.model.access.csv',
        'views/account_analytic_account.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
