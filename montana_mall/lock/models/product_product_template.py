from odoo import models, fields, api

class ProductProductTemplate(models.Model):
    _inherit = 'product.template'

    si_locked = fields.Boolean(string='Locked', default=False)

    def si_set_locked(self):
        """Toggle the locked state."""
        for record in self:
            record = record.with_context(si_set_locked=True)
            record.si_locked = not record.si_locked
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.model
    def create(self, values):
        """Ensure locked is False on creation."""
        values['si_locked'] = values.get('si_locked', False)
        return super(ProductProductTemplate, self).create(values)

    def write(self, values):
        """Prevent locked from being unintentionally modified."""
        if not self.env.context.get('si_set_locked'):
            values.pop('si_locked', None)
        return super(ProductProductTemplate, self).write(values)
