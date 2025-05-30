from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    si_locked = fields.Boolean(string='Locked', default=False)

    def si_set_locked(self):
        """Toggle the si_locked state."""
        for record in self:
            record = record.with_context(si_set_locked=True)
            record.si_locked = not record.si_locked
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_confirm(self):
        """Extend action_confirm to lock the form."""
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            record = record.with_context(si_set_locked=True)
            record.si_locked = True
        return res

    @api.model
    def create(self, values):
        """Ensure si_locked is False on creation."""
        values['si_locked'] = values.get('si_locked', False)
        return super(SaleOrder, self).create(values)

    def write(self, values):
        """Prevent si_locked from being unintentionally modified."""
        if not self.env.context.get('si_set_locked'):
            values.pop('si_locked', None)
        return super(SaleOrder, self).write(values)


    def set_locked(self):
        """Toggle the si_locked state."""
        for record in self:
            record = record.with_context(set_locked=True)
            record.si_locked = not record.si_locked
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_confirm(self):
        """Extend action_confirm to lock the form."""
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            record = record.with_context(set_locked=True)
            record.si_locked = True
        return res

    @api.model
    def create(self, values):
        """Ensure si_locked is False on creation."""
        values['si_locked'] = values.get('si_locked', False)
        return super(SaleOrder, self).create(values)

    def write(self, values):
        """Prevent si_locked from being unintentionally modified."""
        if not self.env.context.get('set_locked'):
            values.pop('si_locked', None)
        return super(SaleOrder, self).write(values)

