# -*- coding: utf-8 -*-

from odoo import models, fields, api
#
#
from odoo.addons.test_convert.tests.test_env import data


class CustomPdf(models.Model):
    _name = 'custom.pdf'
    _description = 'custom_pdf.custom_pdf'

    name = fields.Char()
    value = fields.Integer()

    def action_create_pdf(self):
        print('hellow world im here')

class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    # def action_create_pdf(self):
    #     print('hellow world im here')
    #     report = self.env['ir.actions.report']._for_xml_id('custom_pdf.hotel_custom_pdf')
        # print('report....', report)
        # return report
        # return self.env.ref('sale.action_report_saleorder').report_action([1])
        # return self.env.ref('custom_pdf.hotel_custom_pdf').report_action(self,id)
        # return self.env['ir.actions.report']._for_xml_id('custom_pdf.hotel_custom_pdf')
