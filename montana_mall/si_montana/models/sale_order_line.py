from odoo import models, api
from dateutil.relativedelta import relativedelta
from odoo.tools import format_date
import calendar

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        """Prepare invoice lines and apply rent description only to rental products."""
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)

        rental_category = self.env['product.category'].search([('name', '=', 'Rent')], limit=1)

        if self.product_id.categ_id == rental_category:
            base_date = self.order_id.next_invoice_date or self.order_id.date_order.date()
            start_date = base_date.replace(day=1)
            
            last_day = calendar.monthrange(start_date.year, start_date.month)[1]
            end_date = start_date.replace(day=last_day)

            start_date_str = format_date(self.env, start_date)
            end_date_str = format_date(self.env, end_date)

            res['name'] = f"Rent - 1 Month {start_date_str} to {end_date_str}"

        return res
