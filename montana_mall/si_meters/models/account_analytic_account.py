from odoo import models, fields, api

class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    si_meter_number = fields.Many2one(
        'si.meters',
        string="Meter Number",
        domain="[('si_status', '=', 'active'), ('availability', '=', 'available')]",
        help="Select an active meter number."
    )
    si_meter_status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')],
        string="Meter Status",
        readonly=True,
        help="Displays the operational status of the selected meter."
    )
    date_allocated = fields.Date(string="Date Allocated", required=True)
    token_units = fields.Float(string="Token Units", required=False)
    comments = fields.Text(string="Comments")
    
    @api.onchange('si_meter_number')
    def _onchange_si_meter_number(self):
        if self.si_meter_number:
            self.si_meter_number.write({
                'allocated_unit_id': self.id,
                'availability': 'unavailable'
            })
            self.si_meter_status = self.si_meter_number.si_status
        else:
            self.si_meter_status = False

    def write(self, vals):
        for record in self:
            if 'si_meter_number' in vals:
                new_meter = vals.get('si_meter_number')
                if record.si_meter_number and not new_meter:
                    record.si_meter_number.write({
                        'allocated_unit_id': False,
                        'availability': 'available'
                    })
                if new_meter:
                    self.env['si.meters'].browse(new_meter).write({
                        'allocated_unit_id': record.id,
                        'availability': 'unavailable'
                    })

        return super(AccountAnalyticAccount, self).write(vals)
