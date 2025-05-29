from . import models

from odoo import models, fields, api, SUPERUSER_ID

def update_existing_scraps(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    scrap_ids = env['stock.scrap'].search([('state', '=', None)])
    
    for scrap in scrap_ids:
        scrap.write({
            'state': 'awaiting',
            'has_approval_request': True,
            'requested_by': SUPERUSER_ID,
        })
