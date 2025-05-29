{
    "name": "Scrap Approval Request",
    "version": "16.0.1.0",
    "depends": ["base", "stock"],
    "author": "iBOS",
    "category": "Inventory",
    "description": "Requires approval for scrapping stock.",
    'data': [
    'security/scrap_security.xml',
    'security/ir.model.access.csv',
    'views/stock_scrap_views.xml',
    ],
    'post_init_hook':'update_existing_scraps',
    'images': ['static/description/icon.png'],
    "installable": True,
}
