from babel.dates import format_date
from odoo import models, fields, api, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('product_id')
    def _compute_name(self):
        term_by_move = (self.move_id.line_ids | self).filtered(lambda l: l.display_type == 'payment_term')\
            .sorted(lambda l: l.date_maturity if l.date_maturity else date.max).grouped('move_id')

        for line in self.filtered(lambda l: l.move_id.inalterable_hash is False):
            if line.display_type == 'payment_term':
                term_lines = term_by_move.get(line.move_id, self.env['account.move.line'])
                n_terms = len(line.move_id.invoice_payment_term_id.line_ids)
                name = line.move_id.payment_reference or ''
                if n_terms > 1:
                    index = term_lines._ids.index(line.id) if line in term_lines else len(term_lines)
                    name = _('%s installment #%s', name, index + 1).lstrip()
                line.name = name

            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue

            if line.partner_id.lang:
                product = line.product_id.with_context(lang=line.partner_id.lang)
            else:
                product = line.product_id

            # Get the start date (either from the line's maturity date or the invoice's date)
            start_date = line.date_maturity or line.move_id.invoice_date or line.move_id.date

            if start_date:
                # Calculate the start and end dates for the rent period
                start_date = start_date.replace(day=1)  # Set the start to the first of the month
                end_date = start_date + relativedelta(day=31)  # Get the last day of the same month

                # Format the period as "Rent - 1 Month 01/01/2025 to 31/01/2025"
                month_year = format_date(start_date, format='MMMM yyyy', locale=line.partner_id.lang or 'en_US')
                label = f"Rent - 1 Month {start_date.day:02d}/{start_date.month:02d}/{start_date.year} to {end_date.day:02d}/{end_date.month:02d}/{end_date.year}"
                
                # Assign the generated label to the name field
                line.name = label
            else:
                # Fallback to the regular product name if there's no valid date
                values = []
                if product.partner_ref:
                    values.append(product.partner_ref)
                if line.journal_id.type == 'sale' and product.description_sale:
                    values.append(product.description_sale)
                elif line.journal_id.type == 'purchase' and product.description_purchase:
                    values.append(product.description_purchase)
                line.name = '\n'.join(values)
                
                
                
    @api.model
    def update_invoice_line_descriptions(self):
        """Update the invoice line descriptions for rental products."""
        invoice_lines = self.env['account.move.line'].search([
            ('name', 'not like', 'Rent - 1 Month%'),
            ('move_id.state', '=', 'posted'),  # Filter for posted invoices
            ('product_id', '!=', False)       # Ensure it's a product line
        ])
        
        for line in invoice_lines:
            # Ensure invoice_date is a proper date object
            invoice_date = line.move_id.invoice_date or line.move_id.date
            if not isinstance(invoice_date, datetime):
                invoice_date = datetime.combine(invoice_date, datetime.min.time())
            
            # Calculate start_date and end_date
            start_date = invoice_date.replace(day=1)
            end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
            
            # Format dates as strings
            start_date_str = format_date(self.env, start_date.date())
            end_date_str = format_date(self.env, end_date.date())
            
            # Update the line's name
            description = f"Rent - 1 Month {start_date_str} to {end_date_str}"
            line.name = description


