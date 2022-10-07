import base64
import io
from odoo import models

class AnnexureReportXlsx(models.AbstractModel):
    _name='report.annexure_c_report.report_annexure_c'
    _inherit='report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, args):
        sheet = workbook.add_worksheet('Annexure C')
        row, col = 6,0
        format_head = workbook.add_format({'align': 'center', 'bold':True,  'font':180,  'bg_color': 'silver'})
        format_sub_head = workbook.add_format({'align': 'center', 'bold':True,  'font':180,  'bg_color': 'silver'})
        row_head = 0
        col_head = 0
        sheet.merge_range(row_head, col_head, row_head + 2, col_head + 15, 'Annexure C Report', format_head)
        row_sub_head = 3
        col_sub_head = 0
        string ="From " + str(data['start_at']) + " To " + str(data['stop_at'])
        sheet.merge_range(row_sub_head, col_sub_head, row_sub_head , col_sub_head + 15, string, format_sub_head)
        align = workbook.add_format({'align': 'center'})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'silver'})
        sheet.write(row, col, 'Serail Number', format_1)
        sheet.write(row, col+1, 'NTN', format_1)
        sheet.write(row, col+2, 'CNIC', format_1)
        sheet.write(row, col+3, 'Name Of Buyer', format_1)
        sheet.write(row, col+4, 'District Of Buyer', format_1)
        sheet.write(row, col+5, 'Buyer Type', format_1)
        sheet.write(row, col+6, 'Document Type', format_1)
        sheet.write(row, col+7, 'Document Number', format_1)
        sheet.write(row, col+8, 'Document Date', format_1)
        sheet.write(row, col+9, 'HS Code', format_1)
        sheet.write(row, col+10, 'Sale Type', format_1)
        sheet.write(row, col+11, 'Rate', format_1)
        sheet.write(row, col+12, 'Value Of Sales\n Excluding Sales\n Tax', format_1)
        sheet.write(row, col+13, 'Sales Tax Involved', format_1)
        sheet.write(row, col+14, 'Quantity', format_1)
        sheet.write(row, col+15, 'ST Withheld at Source', format_1)
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 20)
        sheet.set_column('K:K', 20)
        sheet.set_column('L:L', 20)
        sheet.set_column('M:M', 20)
        sheet.set_column('N:N', 20)
        sheet.set_column('O:O', 20)
        sheet.set_column('P:P', 20)
        rec_row, rec_col = 7,0
        serial_number = 1
        for rec in data['purchase_records']:
            sheet.write(rec_row, rec_col, serial_number)
            sheet.write(rec_row, rec_col+1, rec['ntn'])
            sheet.write(rec_row, rec_col+3, rec['customer_name'])
            sheet.write(rec_row, rec_col+5, "SI", align)
            sheet.write(rec_row, rec_col+7, rec['document_name'])
            sheet.write(rec_row, rec_col+8, rec['invoice_date'])
            sheet.write(rec_row, rec_col+12, rec['untaxed_amount'])
            sheet.write(rec_row, rec_col+13, rec['tax'])
            sheet.write(rec_row, rec_col+14, rec['quantity'])
            serial_number += 1
            rec_row += 1