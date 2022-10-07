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


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_amount(self):
        for move in self:

            if move.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                move.payment_state = move.payment_state
                continue

            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_to_pay = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = move._get_lines_onchange_currency().currency_id

            for line in move.line_ids:
                if move.is_invoice(include_receipts=True):
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_to_pay += line.balance
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency

            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
            move.amount_total = sign * (total_currency if len(currencies) == 1 else total)
            move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
            move.amount_untaxed_signed = -total_untaxed
            move.amount_tax_signed = -total_tax
            move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
            move.amount_residual_signed = total_residual
            move.amount_total = move.amount_total + move.shipping_rate

            currency = len(currencies) == 1 and currencies or move.company_id.currency_id

            # Compute 'payment_state'.
            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

            if move.is_invoice(include_receipts=True) and move.state == 'posted':

                if currency.is_zero(move.amount_residual):
                    reconciled_payments = move._get_reconciled_payments()
                    if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency.compare_amounts(total_to_pay, total_residual) != 0:
                    new_pmt_state = 'partial'

            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
                reverse_moves = self.env['account.move'].search(
                    [('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

                # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
                reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (
                        reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'

            move.payment_state = new_pmt_state

    @api.depends('amount_total', 'discount_rate', 'discount_type', 'shipping_cost')
    def _compute_net_total(self):
        for each in self:
            if each.amount_total > 0:
                if each.discount_type == 'fixed_amount':
                    if each.discount_rate <= each.amount_total:
                        each.discount = each.discount_rate
                    else:
                        raise UserError(_("Discount Cannot be more than Total"))
                elif each.discount_type == 'percentage_discount':
                    if each.discount_rate <= 100:
                        each.discount = (each.amount_total * each.discount_rate) / 100
                    else:
                        raise UserError(_("Discount rate cannot be more than 100%"))
                each.shipping_cost = each.shipping_rate
                each.net_total = each.amount_total - each.discount
            else:
                each.shipping_cost = 0
                each.discount = 0
                each.net_total = 0

    # shipping_cost = fields.Monetary(string="Shipping Charges", store=True)
    shipping_cost = fields.Monetary(string="Shipping Charges", compute='_compute_net_total')
    shipping_rate = fields.Float(string="Shipping Charges")
    discount_type = fields.Selection([('fixed_amount', 'Fixed Amount'),
                                      ('percentage_discount', 'Percentage')],
                                     string="Discount Type")
    discount_rate = fields.Float(string="Discount Rate")
    discount = fields.Monetary(string="Discount", compute='_compute_net_total')
    net_total = fields.Monetary(string="Net Total", compute='_compute_net_total')

    def action_post(self):
        for move in self:
            sale = (self.env['sale.order'].browse(self._context.get('active_id')) if move.discount_rate == 0 else move)
            if move and move.move_type == 'out_invoice' and not move.line_ids.filtered(
                    lambda line: line.name == ('Discount Amount')):
                discount_account_id = int(self.env['ir.config_parameter'].sudo().get_param('sales_discount_account_id'))
                if move.discount_rate > 0:
                    if not discount_account_id:
                        raise UserError(_('Please select sale/purchase discount account first in accounting settings.'))
                    else:
                        ml = {'account_id': discount_account_id,
                              'name': 'Discount Amount',
                              'partner_id': move.partner_id.id,
                              'move_id': move.id,
                              'exclude_from_invoice_tab': True,
                              'currency_id': move.currency_id.id
                              }
                        self.write({'invoice_line_ids': [(0, 0, ml)]})

                elif sale.discount_rate > 0:
                    if not discount_account_id:
                        raise UserError(
                            _('Please select sale/purchase discount charges account first in accounting settings.'))
                    else:
                        ml = {'account_id': discount_account_id,
                              'name': 'Discount Amount',
                              'partner_id': move.partner_id.id,
                              'move_id': move.id,
                              'exclude_from_invoice_tab': True,
                              'currency_id': move.currency_id.id
                              }
                        self.write({'invoice_line_ids': [(0, 0, ml)]})
                if move and move.move_type == 'out_invoice' and not move.line_ids.filtered(
                        lambda line: line.name == ('Shipping Charges')):
                    shipping_account_id = int(
                        self.env['ir.config_parameter'].sudo().get_param('sale_shipping_account_id'))
                    if move.shipping_rate > 0:
                        if not shipping_account_id:
                            raise UserError(
                                _('Please select Sale shipping charges first in accounting settings.'))
                        else:
                            ml = {'account_id': shipping_account_id,
                                  'name': 'Shipping Charges',
                                  'partner_id': move.partner_id.id,
                                  'move_id': move.id,
                                  'exclude_from_invoice_tab': True,
                                  'currency_id': move.currency_id.id
                                  }
                            self.write({'invoice_line_ids': [(0, 0, ml)]})
                # elif sale.shipping_rate > 0:
                #     if not shipping_account_id:
                #         raise UserError(_('Please select Sale shipping charges first in accounting settings.'))
                #     else:
                #         ml = {'account_id': shipping_account_id,
                #               'name': 'Discount Amount',
                #               'partner_id': move.partner_id.id,
                #               'move_id': move.id,
                #               'exclude_from_invoice_tab': True,
                #               }
                #         self.write({'invoice_line_ids': [(0, 0, ml)]})
            if move and move.move_type == 'in_invoice' and not move.line_ids.filtered(
                    lambda line: line.name == ('Discount Amount')):
                discount_account_id = int(
                    self.env['ir.config_parameter'].sudo().get_param('purchase_discount_account_id'))
                if move.discount_rate > 0:
                    if not discount_account_id:
                        raise UserError(_('Please select sale/purchase discount account first in accounting settings.'))
                    else:
                        ml = {'account_id': discount_account_id,
                              'name': 'Discount Amount',
                              'partner_id': move.partner_id.id,
                              'move_id': move.id,
                              'exclude_from_invoice_tab': True,
                              'currency_id': move.currency_id.id
                              }
                        self.write({'invoice_line_ids': [(0, 0, ml)]})
            if move and move.move_type == 'in_invoice' and not move.line_ids.filtered(
                    lambda line: line.name == ('Shipping Charges')):
                shipping_account_id = int(
                    self.env['ir.config_parameter'].sudo().get_param('purchase_shipping_account_id'))
                if move.shipping_rate > 0:
                    if not shipping_account_id:
                        raise UserError(
                            _('Please select Purchase shipping charges account first in accounting settings.'))
                    else:
                        ml = {'account_id': shipping_account_id,
                              'name': 'Shipping Charges',
                              'partner_id': move.partner_id.id,
                              'move_id': move.id,
                              'exclude_from_invoice_tab': True,
                              'currency_id': move.currency_id.id
                              }
                        self.write({'invoice_line_ids': [(0, 0, ml)]})
            to_write = {
                'line_ids': []
            }
            if move.move_type == 'in_invoice':
                if move.discount_rate > 0:
                    for line in move.line_ids.filtered(
                            lambda line: line.name == ('Discount Amount')):
                        to_write['line_ids'].append((1, line.id, {'credit': move.currency_id._convert(
                            move.discount, self.env.company.currency_id, self.env.company, fields.Date.today())}))
                    # for line in move.line_ids.filtered(
                    #         lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')):
                    #     to_write['line_ids'].append((1, line.id, {'credit': move.line_ids[0].amount_residual/move.line_ids[0].amount_currency * move.amount_total + move.line_ids[0].amount_residual/move.line_ids[0].amount_currency * move.discount}))
                if move.shipping_rate > 0:
                    for line in move.line_ids.filtered(
                            lambda line: line.name == ('Shipping Charges')):
                        # to_write['line_ids'].append((1, line.id, {'debit': move.line_ids[0].amount_residual/move.line_ids[0].amount_currency * move.shipping_cost}))
                        to_write['line_ids'].append((1, line.id, {
                            'debit': move.currency_id._convert(
                                move.shipping_cost, self.env.company.currency_id, self.env.company,
                                fields.Date.today())}))
                for line in move.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')):
                    to_write['line_ids'].append((1, line.id, {'credit': move.currency_id._convert(
                        move.net_total, self.env.company.currency_id, self.env.company, fields.Date.today())}))
            elif move.move_type == 'out_invoice':
                if move.discount_rate > 0:
                    for line in move.line_ids.filtered(
                            lambda line: line.name == ('Discount Amount')):
                        to_write['line_ids'].append((1, line.id, {'debit': move.discount}))
                    for line in move.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')):
                        to_write['line_ids'].append((1, line.id, {'debit': move.net_total}))
                if move.shipping_rate > 0:
                    for line in move.line_ids.filtered(
                            lambda line: line.name == ('Shipping Charges')):
                        to_write['line_ids'].append((1, line.id, {
                            'credit': move.currency_id._convert(
                                move.shipping_cost, self.env.company.currency_id, self.env.company,
                                fields.Date.today())}))
                        # to_write['line_ids'].append((1, line.id, {'debit': move.shipping_cost}))
                    for line in move.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')):
                        to_write['line_ids'].append((1, line.id, {'debit': move.net_total}))
            move.write(to_write)
        rec = super(AccountMove, self).action_post()
        return rec

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
