# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import odoo.addons.decimal_precision as dp
from string import digits



# from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class CompanyEXT(models.Model):
    _inherit = 'res.company'

    company_strn = fields.Char('STRN Number')
    sale_qf_code = fields.Char('Sale QF-Code')
    invoice_qf_code = fields.Char('Invoice QF-Code')
    Delivery_qf_code = fields.Char('Delivery QF-Code')
    purchase_qf_code = fields.Char('Purchase QF-Code')
    logo_sale = fields.Binary('Sale Report Logo', help="Display this logo on the website.")
    logo_invoice = fields.Binary('Invoice Report Logo', help="Display this logo on the website.")
    logo_Delivery = fields.Binary('Delivery Report Logo', help="Display this logo on the website.")
    logo_purchase = fields.Binary('Purchase Report Logo', help="Display this logo on the website.")
    invoice_text = fields.Text(string='Withholding Tax Not To Be Deducted')
    invoice_text_2 = fields.Text(string='Mode of Payment')

class PARTNEREXT(models.Model):
    _inherit = 'res.partner'

    gender_type = fields.Selection([
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Miss.', 'Miss.')
    ], string="Gender Titles")
    # gender_type = fields.Char(string='Gender Titles')
    account_no = fields.Char(string='Account NO City Wise')


class Delivery_reports(models.Model):
    _inherit = 'stock.picking'

    end_user = fields.Many2one(related='sale_id.end_user', readonly=False, store=True)
    # end_user = fields.Many2one('res.partner', string='End User')



class Sale_report(models.Model):
    _inherit = 'sale.order'

    manufacturer = fields.Char('Manufacturer')


class AccountMove(models.Model):
    _inherit = 'account.move'


class PurchaseOrderExt(models.Model):
    _inherit = 'purchase.order'

    ship_to = fields.Many2one('res.partner', string='Ship To')
    invoice_to = fields.Many2one('res.partner', string='Invoice To')


class PurchaseLineCodeExt(models.Model):
    _inherit = 'purchase.order.line'

    default_code = fields.Char(related='product_id.default_code', store=True, string="Product Code")
