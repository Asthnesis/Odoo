from . import models
from odoo import api, SUPERUSER_ID

def modify_existing_boms(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    boms = env['mrp.bom'].search([('state', '=', 'draft')])
    for bom in boms:
        bom.write({
            'state': 'pending',
            'has_approval_request': True,
            'requested_by': SUPERUSER_ID, 
        })
