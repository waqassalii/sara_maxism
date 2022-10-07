# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import api, fields, models, _


class DiscountConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sales_discount_account_id = fields.Many2one('account.account',
                                                string="Sales Discount Account")
    purchase_discount_account_id = fields.Many2one('account.account',
                                                   string="Purchase Discount Account")

    purchase_shipping_account_id = fields.Many2one('account.account',
                                                   string="Shipping Charges Account")

    sale_shipping_account_id = fields.Many2one('account.account',
                                                   string="Shipping Charges Account")

    def get_values(self):
        res = super(DiscountConfigSetting, self).get_values()
        res.update({'sales_discount_account_id': 
                            int(self.env['ir.config_parameter'].sudo().get_param('sales_discount_account_id')) or False,
                    'purchase_discount_account_id': 
                            int(self.env['ir.config_parameter'].sudo().get_param('purchase_discount_account_id'))or False,
                    'purchase_shipping_account_id':
                    int(self.env['ir.config_parameter'].sudo().get_param('purchase_shipping_account_id')) or False,
                    'sale_shipping_account_id':
                        int(self.env['ir.config_parameter'].sudo().get_param('sale_shipping_account_id')) or False,
                    })
        return res

    def set_values(self):
        res = super(DiscountConfigSetting, self).set_values()
        if self.sales_discount_account_id:
            self.env['ir.config_parameter'].sudo().set_param('sales_discount_account_id',
                                                                 self.sales_discount_account_id.id or False)
        if self.purchase_discount_account_id:
            self.env['ir.config_parameter'].sudo().set_param('purchase_discount_account_id',
                                                                self.purchase_discount_account_id.id or False)
        if self.purchase_shipping_account_id:
            self.env['ir.config_parameter'].sudo().set_param('purchase_shipping_account_id',
                                                                self.purchase_shipping_account_id.id or False)
        if self.sale_shipping_account_id:
            self.env['ir.config_parameter'].sudo().set_param('sale_shipping_account_id',
                                                                self.sale_shipping_account_id.id or False)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
