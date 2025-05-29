{
    "name": "Scrap Approval Request",
    "version": "17.0.1.0",
    "depends": ["base", "stock"],
    "author": "iBOS",
    "category": "Inventory",
    "description": "Approval requests when scrapping products",
    'data': [
    'security/scrap_security.xml',
    'security/ir.model.access.csv',
    'views/stock_scrap_views.xml',
    ],
    'post_init_hook':'update_existing_scraps',
    'uninstall_hook':'uninstall_hook',
    'images': ['static/description/icon.png'],
    "installable": True,
}
