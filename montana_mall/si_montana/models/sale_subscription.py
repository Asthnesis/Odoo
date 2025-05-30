from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    si_invoice_status = fields.Selection(
        selection=[
            ('upselling', 'Upselling Opportunity'),
            ('invoiced', 'Fully Invoiced'),
            ('to invoice', 'To Invoice'),
            ('no', 'Nothing to Invoice')
        ],
        string="Invoice Status",
        compute="_compute_si_invoice_status",
        store=True
    )

    @api.depends('invoice_status')
    def _compute_si_invoice_status(self):
        for order in self:
            order.si_invoice_status = order.invoice_status
