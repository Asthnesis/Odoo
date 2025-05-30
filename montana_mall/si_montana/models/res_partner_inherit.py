from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    linked_units_info = fields.Text(
        string="Linked Units",
        compute="_compute_linked_units_info",
        readonly=True
    )
    
    si_unit_customer_link = fields.One2many(
        comodel_name='account.analytic.account',
        inverse_name='si_customer',
        string='Units Owned',
        compute='_compute_si_unit_customer_link'
    )

    @api.depends('si_unit_customer_link.si_customer')
    def _compute_si_unit_customer_link(self):
        for partner in self:
            partner.si_unit_customer_link = self.env['account.analytic.account'].search([
                ('si_customer', '=', partner.id)
            ])
    

    def _compute_linked_units_info(self):
        for partner in self:
            linked_units = self.env['account.analytic.account'].search([
                ('si_customer', '=', partner.id)
            ])
            partner.linked_units_info = "\n".join(linked_units.mapped('name')) if linked_units else "No linked units."
    
    @api.model
    def create(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()  
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()  
        if 'email' in vals:
            vals['email'] = vals['email'].lower()
        
        if 'vat' in vals and vals['vat']:
            vat = vals['vat']
            if len(vat) > 2:
                vals['vat'] = vat[0].upper() + vat[1:-1] + vat[-1].upper()
            else:
                vals['vat'] = vat.upper()

        return super(ResPartner, self).write(vals)

    @api.constrains('email', 'phone', 'mobile', 'vat')
    def _check_partner_details(self):
        for record in self:
            if record.email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', record.email):
                raise ValidationError("Please provide a valid email address.")

            if record.phone and (not record.phone.isdigit() or len(record.phone) != 10 or not record.phone.startswith('0')):
                raise ValidationError("Phone number must contain exactly 10 digits and start with 0.")

            if record.mobile and (not record.mobile.isdigit() or len(record.mobile) != 10 or not record.mobile.startswith('0')):
                raise ValidationError("Mobile number must contain exactly 10 digits and start with 0.")
           
            if record.vat:
                if not re.match(r'^[A-Z]\d{9}[A-Z]$', record.vat):
                    raise ValidationError(
                        "Tax ID must be 11 characters long with the first and last being capital letters and the middle 9 being digits."
                    )
