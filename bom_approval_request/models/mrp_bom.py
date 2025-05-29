from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    
    
    has_approval_request = fields.Boolean(string="Has Approval Request", default=False)
    
    bom_id = fields.Many2one('mrp.bom', required=True, ondelete='cascade')
    requested_by = fields.Many2one('res.users', readonly=True, string="Requested By")
    approved_by = fields.Many2one('res.users', string="Reviewed By", readonly=True)
    date_requested = fields.Datetime(string="Date Requested")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', required=True, readonly=True, copy=False,
       tracking=True, default='draft')

    def button_pending(self):
        for bom in self:
            if bom.state != 'draft':
                raise UserError("Only BOMs in draft state can request approval.")
            bom.write({
                'state': 'pending',
                'requested_by': self.env.user.id,
                'date_requested': fields.Datetime.now(),
            })

            group = self.env.ref('bom_approval_request.group_bom_approver')
            approvers = group.users
            if approvers:
                bom.message_subscribe(partner_ids=approvers.mapped('partner_id').ids)

                bom.message_post(
                    body=_("Approval requested."),
                    message_type='notification',
                    subtype_xmlid='mail.mt_note',
                    notify=True,
                    partner_ids=approvers.mapped('partner_id').ids,
                )
                
    def action_approve(self):
        for bom in self.filtered(lambda b: b.state == 'pending'):
            bom.write({
                'state': 'approved',
                'approved_by': self.env.user.id,
            })

    def action_reject(self):
        for bom in self.filtered(lambda b: b.state == 'pending'):
            bom.write({
                'state': 'rejected',
                'approved_by': self.env.user.id,
            })
    def action_draft(self):
        for bom in self:
            bom.write({
                'state': 'draft',
                'has_approval_request': False,
            })
