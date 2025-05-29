from . import models

from odoo import  SUPERUSER_ID

def update_existing_scraps(env):
    scrap_ids = env['stock.scrap'].search([('state', '=', None)])
    
    for scrap in scrap_ids:
        scrap.write({
            'state': 'awaiting',
            'has_approval_request': True,
            'requested_by': SUPERUSER_ID,
        })
def uninstall_hook(env):
    scraps = env['stock.scrap'].search([('state', 'in', ['awaiting', 'awaiting_finance'])])
    scraps.write({
        'state': 'draft',
        'requested_by': env.uid,
    })
