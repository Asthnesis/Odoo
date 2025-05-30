# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
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

from odoo import fields, api,models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    status = fields.Selection([('draft', 'Draft'), ('awaiting', 'Awaiting Approval'), ('approve', 'Approved'),
                              ("reject", "Rejected")], default='draft', help='Status of the contact',
                             tracking=True)

    approver_id = fields.Many2one(
        'res.users', string="Approved By", readonly=True,  help='Person responsible for validating the contacts.')

    def action_approve_contact(self):
        """Manager validating the contacts."""
        if self.env.user.has_group(
                'odoo_contact_approval.group_contacts_approval'):
            self.write({
                'status': "approve",
                'approver_id': self.env.uid
            })
        else:
            raise UserError(_(
                "You do not have the access right to Contacts Approval."
                " Please contact your administrator.")
            )

    def action_reject_contact(self):
        """Manager Rejecting the contacts."""
        if self.env.user.has_group(
                'odoo_contact_approval.group_contacts_approval'):
            self.write({
                'status': "reject",
                'approver_id': None
            })
        else:
            raise UserError(_(
                "You do not have the access right to Contacts Approval."
                " Please contact your administrator.")
            )

    def action_reset_contact(self):
        """Manager resetting the contacts."""
        if self.env.user.has_group(
                'odoo_contact_approval.group_contacts_approval'):
            self.write({
                'status': "draft",
                'approver_id': None
            })
        else:
            raise UserError(_(
                "You do not have the access right to Contacts Approval."
                " Please contact your administrator.")
            )
    def action_approve(self):
        for partner in self:
            if partner.status == 'draft':
                partner.write({
                'status': "awaiting",
                'approver_id': None
            })
                group = self.env.ref('odoo_contact_approval.group_contacts_approval', raise_if_not_found=False)
                if group:
                    approvers = group.users
                    if approvers:
                        partner.message_subscribe(partner_ids=approvers.mapped('partner_id').ids)

                        template = self.env.ref('odoo_contact_approval.email_template_contact_approval_request', raise_if_not_found=False)
                        if template:
                            template.send_mail(partner.id, force_send=True, raise_exception=True)

                        partner.message_post(
                            body=_("Approval requested."),
                            message_type='notification',
                            subtype_xmlid='mail.mt_note',
                            notify=True,
                            partner_ids=approvers.mapped('partner_id').ids,
                        )