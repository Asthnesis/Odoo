from odoo import models, fields, api,_
from odoo.exceptions import UserError
from datetime import datetime

class StockScrap(models.Model):
    _inherit = ['stock.scrap', 'mail.thread']
    _name = 'stock.scrap'

    requested_by = fields.Many2one('res.users', readonly=True, string="Requested By")
    hod_approved_by = fields.Many2one('res.users', string="Scrap HOD Reviewer", readonly=True) 
    fin_approved_by = fields.Many2one('res.users', string="Scrap Finance Reviewer", readonly=True)  
    rejected_by = fields.Many2one('res.users', string="Rejected By", readonly=True)  
    scrap_id = fields.Many2one('stock.scrap', required=True, ondelete='cascade')
    date_requested = fields.Datetime(string="Date Requested", default=fields.Datetime.now)
    quantity = fields.Float(string="Quantity", related='scrap_id.scrap_qty', store=True)
    has_approval_request = fields.Boolean(string="Has Approval Request", default=False)    
    reason = fields.Char(string="Reason for Scrapping")
    state = fields.Selection(selection_add=[
        ('awaiting', 'Awaiting HOD Approval'),
        ('awaiting_finance', 'Awaiting Finance Approval'),
        ('rejected', 'Rejected'),
        ('done', 'Approved'),
    ])
    
    def action_hod_approve(self):
        for rec in self.filtered(lambda b: b.state == 'awaiting'):
            rec.hod_approved_by = self.env.user.id
            rec.state = 'awaiting_finance'

    # Finance approval action
    def action_validate(self):
        for rec in self.filtered(lambda s: s.state == 'awaiting_finance'):
            rec.fin_approved_by = self.env.user.id
            rec.state = 'done'
            super(StockScrap, rec).action_validate()

    def action_reject(self):
        for rec in self.filtered(lambda b: b.state in ['awaiting', 'awaiting_finance']):
            rec.state = 'rejected'
            rec.rejected_by = self.env.user.id
            
    def action_draft(self):
        for rec in self:
            rec.write({
                'state': 'draft',
                'has_approval_request': False,
            })


    def action_request(self):
        for rec in self:
            if not rec.has_approval_request:
                if not rec.name or rec.name == 'New':
                    rec.name = self.env['ir.sequence'].next_by_code('stock.scrap')

                rec.write({
                    'state': 'awaiting',
                    'has_approval_request': True,
                    'requested_by': self.env.user.id,
                    'date_requested': fields.Datetime.now(),
                })

                group_hod = self.env.ref('scrap_approval_request.group_scrap_hod_approver')
                group_finance = self.env.ref('scrap_approval_request.group_scrap_finance_approver')
                followers = (group_hod.users | group_finance.users).mapped('partner_id')
                if followers:
                    rec.message_subscribe(partner_ids=followers.ids)

                    rec.message_post(
                        body=_("A scrap request has been submitted for approval."),
                        message_type='notification',
                        subtype_xmlid='mail.mt_note',
                        partner_ids=followers.ids,
                    )

                rec.has_approval_request = True
            else:
                raise UserError(_("This scrap request is already awaiting approval."))