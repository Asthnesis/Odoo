from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    si_rental_end_date = fields.Date(
        string="Lease End Date",
        compute="_compute_rental_end_date",
        store=True,
        readonly=True,
    )
    lease_picked = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Lease Picked",
        default='no',
    )

    steel_door = fields.Selection(
        [('tenant', 'Tenant'), ('owner', 'Owner')],
        string="Steel Door",
        default='owner',
    )

    shutter_door = fields.Selection(
        [('tenant', 'Tenant'), ('owner', 'Owner')],
        string="Shutter Door",
        default='owner',
    )
    x_account_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string="Unit",
        domain="[('x_is_available', '=', True)]"
    )
    si_unit_customer_link = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Unit',
        domain="[('si_customer', '=', partner_id)]",
    )

    @api.depends('x_rental_start_date')
    def _compute_rental_end_date(self):
        for record in self:
            if record.x_rental_start_date:
                start_date = fields.Date.from_string(record.x_rental_start_date)
                end_date = start_date + relativedelta(years=5)
                end_date = end_date - timedelta(days=1)
                record.si_rental_end_date = end_date
            else:
                record.si_rental_end_date = None
                
                
    @api.onchange('si_unit_customer_link')
    def _onchange_si_unit_customer_link(self):
        """Populate end_date based on the unit selected and the corresponding contract."""
        for order in self:
            if order.si_unit_customer_link:
                contract = self.env['sale.order'].search([
                    ('x_account_analytic_account_id', '=', order.si_unit_customer_link.id),
                    ('state', '=', 'sale')
                ], limit=1)

                if contract and contract.si_rental_end_date:
                    order.end_date = contract.si_rental_end_date
                else:
                    order.end_date = False
            else:
                order.end_date = False
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            available_units = self.env['account.analytic.account'].search([
                ('si_customer', '=', self.partner_id.id),
                ('available_unit', '=', True)
            ])
            self.si_unit_customer_link = available_units[:1] if available_units else False
            return {
                'domain': {'si_unit_customer_link': [
                    ('available_unit', '=', True),
                    ('si_customer', '=', self.partner_id.id)
                ]}
            }
        else:
            self.si_unit_customer_link = False
            self.x_account_analytic_account_id.partner_id = False