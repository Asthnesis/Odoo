from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SiMeters(models.Model):
    _name = 'si.meters'
    _description = 'Meter Tracking'
    _rec_name = "si_meter_number"

    si_meter_number = fields.Char(
        string='Meter Number',
        required=True,
        readonly=False,
        stored = True
    )
    si_status = fields.Selection(
        selection=[('active', 'Active'), ('inactive', 'Inactive')],
        string='Status',
        readonly=False,
        default='active'
    )
    availability = fields.Selection(
        [('available', 'Available'), ('unavailable', 'Unavailable')],
        string="Availability",
        default='available',
        help="Indicates whether the meter is available for allocation."
    )
    date_added = fields.Date(string="Date Added", required=True)
    allocated_unit_id = fields.Many2one(
        'account.analytic.account',
        string="Allocated Unit",
        help="The unit to which this meter is currently allocated."
    )
    _sql_constraints = [
        ('unique_si_meter_number', 'UNIQUE(si_meter_number)', 'Meter Number must be unique.')
    ]

    @api.constrains('si_meter_number')
    def _validate_meter_lines(self):
        for record in self:
            if not record.si_meter_number.isdigit():
                raise ValidationError("Meter Number must be numeric.")
            if len(record.si_meter_number) != 11:
                raise ValidationError("Meter Number must be exactly 11 digits.")
            