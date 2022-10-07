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
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    discount_type = fields.Selection([('fixed_amount', 'Fixed Amount'),
                                      ('percentage_discount', 'Percentage')],
                                     string="Discount Type")
    discount_rate = fields.Float(string="Discount Rate")
    discount = fields.Monetary(string="Discount", compute='_compute_net_total')
    net_total = fields.Monetary(string="Net Total", compute='_compute_net_total')
    shipping_cost = fields.Monetary(string="Shipping Charges", compute='_compute_net_total', store=True)
    shipping_rate = fields.Float(string="Shipping Charges")

    @api.depends('discount_rate', 'amount_total', 'discount_type','shipping_rate')
    def _compute_net_total(self):
        for record in self:
            if record.discount_type == 'fixed_amount':
                if record.discount_rate <= record.amount_total:
                    record.discount = record.discount_rate
                else:
                    raise UserError(_("Discount Cannot be more than Total"))
            elif record.discount_type == 'percentage_discount':
                if record.discount_rate <= 100:
                    record.discount = (record.amount_total * record.discount_rate) / 100
                else:
                    raise UserError(_("Discount rate cannot be more than 100%"))
            record.shipping_cost = record.shipping_rate
            record.net_total = (record.amount_total - record.discount+record.shipping_rate)

    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        self.ensure_one()
        move_type = self._context.get('default_move_type', 'in_invoice')
        journal = self.env['account.move'].with_context(default_move_type=move_type)._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting purchase journal for the company %s (%s).') % (
            self.company_id.name, self.company_id.id))

        partner_invoice_id = self.partner_id.address_get(['invoice'])['invoice']
        invoice_vals = {
            'ref': self.partner_ref or '',
            'move_type': move_type,
            'narration': self.notes,
            'currency_id': self.currency_id.id,
            'invoice_user_id': self.user_id and self.user_id.id,
            'partner_id': partner_invoice_id,
            'fiscal_position_id': (
                        self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(partner_invoice_id)).id,
            'payment_reference': self.partner_ref or '',
            'partner_bank_id': self.partner_id.bank_ids[:1].id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
            # 'end_user':self.end_user.id if self.end_user else False,
        }
        if self.discount_rate and self.discount_type:
            invoice_vals.update({
                'discount_rate': self.discount_rate,
                'discount_type': self.discount_type,
                'discount': self.discount
            })
        if self.shipping_rate:
            invoice_vals.update({
                'shipping_rate': self.shipping_rate,
                'shipping_cost': self.shipping_cost,
            })
        return invoice_vals

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
