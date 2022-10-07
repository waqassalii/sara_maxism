# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
class AccountMove(models.Model):

    _inherit = "account.move"

    advance_payment = fields.Float()
    end_user = fields.Many2one('res.partner')

    @api.onchange('invoice_payment_term_id', 'invoice_date')
    def _onchange_payment_term_date_invoice(self):
        if self.invoice_payment_term_id and self.invoice_date:
            self.invoice_date_due = self.invoice_date + timedelta(self.invoice_payment_term_id.line_ids[0].days)

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    product_code = fields.Char('Product Code', related='product_id.default_code')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue

            # line.name = line._get_computed_name()
            line.name = line.product_id.name
            line.account_id = line._get_computed_account()
            line.tax_ids = line._get_computed_taxes()
            line.product_uom_id = line._get_computed_uom()
            line.price_unit = line._get_computed_price_unit()

            # price_unit and taxes may need to be adapted following Fiscal Position
            line._set_price_and_tax_after_fpos()

            # Convert the unit price to the invoice's currency.
            company = line.move_id.company_id
            line.price_unit = company.currency_id._convert(line.price_unit, line.move_id.currency_id, company,
                                                           line.move_id.date, round=False)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    destination_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Destination Account',
        store=True, readonly=False,
        compute='_compute_destination_account_id',
        domain="[('company_id', '=', company_id)]",
        check_company=True)