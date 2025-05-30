# -*- coding: utf-8 -*-
#############################################################################

#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import fields,api, models,_


class ProductTemplate(models.Model):
    """The module is used to add the approval state in the product form page"""
    _inherit = 'product.template'

    approve_state = fields.Selection([('draft', 'Draft'), ('awaiting', 'Awaiting Approval'), 
                                      ('reject', 'Rejected'),
                                      ('approve', 'Approved')],
                                     default='draft', string='State',
                                     help='State to approve')

    def action_approve_product_approval(self):
        """Approve button on the product form page"""
        for rec in self:
            rec.approve_state = 'approve'

    def action_reset_product_approval(self):
        """Reset to draft state button on the product form page"""
        for rec in self:
            rec.approve_state = 'draft'

    def action_approve_products(self):
        """Bulk product approval button on the product form page"""
        active_ids = self.env.context.get('active_ids')
        products = self.env['product.template'].browse(active_ids)
        products.action_approve_product_approval()
    def action_reject_products(self):
        """Bulk product rejection button on the product form page"""
        active_ids = self.env.context.get('active_ids')
        products = self.env['product.template'].browse(active_ids)
        products.action_reject_product_approval()
        
    def action_reject_product_approval(self):
            self.write({
                'approve_state': "reject",
            })

    def action_request_product_approval(self):
            """Request approval for the product"""
            for product in self:
                if product.approve_state == 'draft':
                    product.write({
                    'approve_state': "awaiting",
                })
                group_mgr = self.env.ref('product_approval_management.product_approval_management_group_manager', raise_if_not_found=False)
                if group_mgr:
                    followers = group_mgr.users.mapped('partner_id')
                    if followers:
                        product.message_subscribe(partner_ids=followers.ids)
                        product.message_post(
                            body=_("A new product has been created and requires approval."),
                            message_type='notification',
                            subtype_xmlid='mail.mt_note',
                            partner_ids=followers.ids,
                        )
            return product
