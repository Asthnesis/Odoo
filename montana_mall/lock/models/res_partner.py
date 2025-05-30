from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    locked = fields.Boolean(string='Locked', default=False)

    def set_locked(self):
        """Toggle the locked state."""
        for record in self:
            record = record.with_context(set_locked=True)
            record.locked = not record.locked
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.model
    def create(self, values):
        """Ensure locked is False on creation."""
        values['locked'] = values.get('locked', False)
        return super(ResPartner, self).create(values)

    def write(self, values):
        """Prevent locked from being unintentionally modified."""
        if not self.env.context.get('set_locked'):
            values.pop('locked', None)
        return super(ResPartner, self).write(values)

