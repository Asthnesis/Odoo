from odoo import models, fields

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    
    si_payment_method = fields.Selection(
        selection=[('mpesa', 'Mpesa'), ('cheque', 'Cheque'), ('cash', 'Cash Deposit'),('bank', 'Bank')],
        string='Payment Method',
        readonly=False,
        default='cheque',
        help = 'Payment method used for this transaction')
