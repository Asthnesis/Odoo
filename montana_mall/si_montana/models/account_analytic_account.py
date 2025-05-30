from odoo import models, fields, api
from datetime import timedelta, datetime

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    si_customer = fields.Many2one(
        'res.partner',
        string="Tenant",
        compute = "_compute_customer",
        store=True,
    )
    sale_order_link = fields.Many2one(
        'sale.order',
        string="Sale Order",
        readonly=True,
    )
    si_location = fields.Selection(
        selection=[('interior', 'Interior'), ('exterior', 'Exterior'), ('rear', 'Rear')],
        string='Location',
        readonly=False,
        default='interior'
    )
    x_is_available = fields.Boolean(
        string="Is Available",
        compute="_compute_is_available",
        store=True,
    )
    available_unit = fields.Boolean(
        string="Available Unit",
        default=True,
        help="Indicates if the unit is available for assignment in a sale order."
    )
    @api.depends('si_customer')
    def _compute_is_available(self):
        for record in self:
            record.x_is_available = not bool(record.si_customer)
    
    @api.depends('x_rental_contract_id')
    def _compute_customer(self):
        for record in self:
            record.si_customer = record.x_rental_contract_id.partner_id if record.x_rental_contract_id else None
            
    @api.model
    def compute_customers_for_contracts(self):
        accounts = self.search([('x_rental_contract_id', '!=', False)])
        for account in accounts:
            account._compute_customer()
            