from datetime import date
from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    si_inv_unit = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Invoiced Unit'
    )
    invoice_date = fields.Date(string="Invoice Date")

    @api.model
    def default_get(self, fields_list):
        """ Ensure invoice_date is set to today's date when creating an invoice. """
        defaults = super().default_get(fields_list)
        if 'invoice_date' in fields_list and not defaults.get('invoice_date'):
            defaults['invoice_date'] = date.today()
        return defaults
    
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.si_unit_customer_link:
            invoice_vals['si_inv_unit'] = self.si_unit_customer_link.id
        return invoice_vals
    
    @api.model
    def create(self, vals):
        """ Ensure si_inv_unit is set when an invoice is created. """
        if not vals.get('si_inv_unit') and vals.get('invoice_origin'):
            sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
            if sale_order and sale_order.si_unit_customer_link:
                vals['si_inv_unit'] = sale_order.si_unit_customer_link.id
        return super().create(vals)

    def write(self, vals):
        """ Update si_inv_unit if it's missing and invoice has a linked sale order. """
        for record in self:
            if 'si_inv_unit' not in vals and not record.si_inv_unit and record.invoice_origin:
                sale_order = self.env['sale.order'].search([('name', '=', record.invoice_origin)], limit=1)
                if sale_order and sale_order.si_unit_customer_link:
                    vals['si_inv_unit'] = sale_order.si_unit_customer_link.id
        return super().write(vals)
    
