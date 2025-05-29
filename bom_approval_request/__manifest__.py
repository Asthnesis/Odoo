{
    "name": "BOM Approval Request",
    "version": "17.0.1.0",
    "depends": ["base", "mrp"],
    "author": "iBOS",
    "category": "Manufacturing",
    "description": "Requires approval for creating BOM.",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/mrp_bom_view.xml',
        'views/mrp_production_form_view.xml',
    ],
    'post_init_hook':'modify_existing_boms',
    'images': ['static/description/icon.png'],
    "installable": True,
    'license': "LGPL-3",
}
