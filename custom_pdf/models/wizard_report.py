from odoo import api, fields, models


class SaleReportWizard(models.TransientModel):
    _name = 'wizard.report'

    # name = fields.Char()

    def action_create_pdf(self):
        return self.env.ref('custom_pdf.hotel_custom_pdf').report_action(self)
    def action_create_xlsx(self):
        return self.env.ref('custom_pdf.xlsx_open_sale_order_xlsx').report_action(self, data={})


class CustomPdfReport(models.AbstractModel):
    _name = 'report.custom_pdf.custom_pdf_qweb'

    @api.model
    def _get_report_values(self, docids, data):
        sale_orders = self.env['sale.order'].search([('state', '=', 'sale'),('invoice_status','!=','invoiced')])
        all_data = []
        single_line = []
        a = 0
        all_order_lines = sale_orders.mapped('order_line')
        products = all_order_lines.mapped('product_id')
        for product in products:
            product_exist_in_lines = all_order_lines.filtered(lambda r: r.product_id.id == product.id)
            all_qty = sum(product_exist_in_lines.mapped('product_uom_qty'))
            a += 1
            single_line.append(a)
            single_line.append(product.default_code)
            single_line.append(product.name)
            single_line.append(all_qty)
            single_line.append(product.qty_available)
            single_line.append(product.qty_available-all_qty)
            all_data.append(single_line)
            single_line = []
        # for order in sale_orders:
        #     for line in order.order_line:
        #         a+=1
        #         single_line.append(a)
        #         single_line.append(line.product_id.default_code)
        #         single_line.append(line.product_id.name)
        #         single_line.append(line.product_uom_qty)
        #         single_line.append(line.product_id.qty_available)
        #         all_data.append(single_line)
        #         single_line = []



        return {
            'all_data': all_data,
        }


class DetailXlsxOpenSaleOrders(models.AbstractModel):
    _name = 'report.custom_pdf.xlsx_open_sale_order_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, report_detail, data):
        normal_text = workbook.add_format({
            "font_color": 'black',
            'font_size': '10',
            'font_name': 'Calibri',
        })
        bold_text = workbook.add_format({
            'bold': 1,
            "font_color": 'black',
            'font_size': '10',
            'font_name': 'Calibri',
        })
        head_blue = workbook.add_format({
            "border": 1,
            'bold': 1,
            "align": 'center',
            "valign": 'vcenter',
            "font_color": 'black',
            "bg_color": '#8faadc',
            'font_size': '10',
            'font_name': 'Calibri',
            # 'num_format': '###0',
        })
        head_yellow = workbook.add_format({
            "border": 1,
            'bold': 1,
            "align": 'center',
            "valign": 'vcenter',
            "font_color": 'black',
            "bg_color": 'yellow',
            'font_size': '10',
            'font_name': 'Calibri',
            # 'num_format': '###0',
        })
        head_white = workbook.add_format({
            "border": 1,
            'bold': 1,
            "align": 'center',
            "valign": 'vcenter',
            "font_color": 'black',
            "bg_color": 'white',
            'font_size': '10',
            'font_name': 'Calibri',
            # 'num_format': '###0',
        })
        head_green = workbook.add_format({
            "border": 1,
            'bold': 1,
            "align": 'center',
            "valign": 'vcenter',
            "font_color": 'black',
            "bg_color": '#e2f0d9',
            'font_size': '10',
            'font_name': 'Calibri',
            # 'num_format': '###0',
        })
        head_red = workbook.add_format({
            "border": 1,
            'bold': 1,
            "align": 'center',
            "valign": 'vcenter',
            "font_color": 'black',
            "bg_color": 'red',
            'font_size': '10',
            'font_name': 'Calibri',
            # 'num_format': '###0',
        })
        format_form_3 = workbook.add_format({
            "border": 1,
            "align": 'center',
            "valign": 'vcenter',
            "font_color": 'black',
            "bg_color": 'white',
            'font_size': '10',
            'font_name': 'Calibri',
        })

        worksheet = workbook.add_worksheet('Open Sale Order Report')
        worksheet.set_column('A:AZ', 20)

        rows = 0
        worksheet.write_string(rows, 0, 'S/N', head_white)
        worksheet.write_string(rows, 1, 'Code', head_white)
        worksheet.write_string(rows, 2, 'Description', head_white)
        worksheet.write_string(rows, 3, 'Total Sale Order Quantity', head_white)
        worksheet.write_string(rows, 4, 'Total Inventory Quantity', head_white)
        worksheet.write_string(rows, 5, 'To Be Arrange', head_white)

        sale_orders = self.env['sale.order'].search([('state', '=', 'sale'), ('invoice_status', '!=', 'invoiced')])
        all_data = []
        single_line = []
        a = 0
        all_order_lines = sale_orders.mapped('order_line')
        products = all_order_lines.mapped('product_id')
        for product in products:
            rows+=1
            product_exist_in_lines = all_order_lines.filtered(lambda r: r.product_id.id == product.id)
            all_qty = sum(product_exist_in_lines.mapped('product_uom_qty'))
            a += 1
            worksheet.write_string(rows, 0, str(a) or '', format_form_3)
            worksheet.write_string(rows, 1, product.default_code or '', format_form_3)
            worksheet.write_string(rows, 2, product.name or '', format_form_3)
            worksheet.write_number(rows, 3, all_qty, format_form_3)
            worksheet.write_number(rows, 4, product.qty_available, format_form_3)
            worksheet.write_number(rows, 5, product.qty_available - all_qty, format_form_3)






