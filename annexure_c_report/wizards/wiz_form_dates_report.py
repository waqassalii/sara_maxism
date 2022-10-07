from odoo import models, fields, api, _

class AnnexWizReport(models.TransientModel):
    _name = 'annexure.reportform'

    def get_excel_report(self):
        annexure_data = None
        if self.start_at and self.stop_at:
            annexure_data = self.env['account.move'].search([('invoice_date','>=', self.start_at),('invoice_date','<=', self.stop_at)])
        elif not self.start_at and not self.stop_at:
            annexure_data = self.env['account.move'].search([])
        elif not self.start_at:
            annexure_data = self.env['account.move'].search([('invoice_date','<=', self.stop_at)])
        elif not self.stop_at:
            annexure_data = self.env['account.move'].search([('invoice_date','>=', self.start_at)])

        lst_records = []
        for rec in annexure_data:
            if rec.state == 'posted' and "INV" in str(rec.name):
                prods_date = {
                    'ntn': rec.partner_id.vat,
                    'customer_name': rec.invoice_partner_display_name,
                    'document_name': rec.name,
                    'invoice_date': rec.invoice_date,
                    'untaxed_amount': rec.amount_untaxed,
                    'total': rec.amount_total,
                    'tax': 0,
                    'quantity': 0
                }
                amount_with_commas = "{:,}".format(prods_date['untaxed_amount'])
                prods_date['untaxed_amount'] = amount_with_commas
                for eles in rec.amount_by_group:
                    prods_date['tax'] = eles[1]
                    for quant in rec.invoice_line_ids:
                        prods_date['quantity'] += quant.quantity
                total_with_commas = "{:,}".format(prods_date['tax'])
                prods_date['tax'] = total_with_commas
                quantity_with_commas = "{:,}".format(prods_date['quantity'])
                prods_date['quantity'] = quantity_with_commas

                lst_records.append(prods_date)
            data = {
                'purchase_records': lst_records,
                'start_at': self.start_at,
                'stop_at': self.stop_at,
                'form_data':self.read()[0]
            }

        return self.env.ref('annexure_c_report.report_annexure_xlsx').report_action(self, data=data)


    start_at = fields.Date(string='Starting Date')
    stop_at = fields.Date(string='Closing Date')