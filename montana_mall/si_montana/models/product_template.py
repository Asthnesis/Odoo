from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].title()
        return super(ProductTemplate, self).create(vals)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].title()
        return super(ProductTemplate, self).write(vals)
