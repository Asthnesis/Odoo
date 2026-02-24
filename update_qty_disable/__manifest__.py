{
    "name": "Disable Update Quantity Feature",
    "version": "18.0.0.2",
    "category": "Warehouse",
    'summary': 'Disabling the update quantity feature on invetory and stock',
    "description": """The "Disable Update Quantity Feature Odoo App" helps users to prevent unauthorized modifications to the quantity of product. This app provides a simple solution for disabling the update quantity feature for certain users in Odoo, Currently in odoo multiple users have access to update the quantity of products, this app provides an effective way to prevent every users from updating the product quantity, Allowed users can only update quantity for products.""",
    'author': 'Edward R',
    "depends": ["stock"],
    "data": [
        'security/product_security.xml',
        'views/product.xml',
    ],
    "license":'LGPL-1',
    "installable": True,
    "application": True,
    "auto_install": False,
    "images": ['static/description/icon.png'],
}