# -*- encoding: utf-8 -*-
##############################################################################
#
#    Bista Solutions Pvt. Ltd
#    Copyright (C) 2019 (http://www.bistasolutions.com)
#
##############################################################################

from odoo import models, fields, _
from odoo.exceptions import UserError


class account_payment(models.Model):
    _inherit = "account.payment"

    write_off_account_ids = fields.One2many(
        'account.payment.write.off', 'account_payment_id',
        string="Write-Off Lines")

    def action_draft(self):
        for payment in self:
            payment.sudo().write_off_account_ids.unlink
        return  super(account_payment, self).action_draft()

    def _prepare_payment_moves(self):
        ''' Prepare the creation of journal entries (account.move) by
        creating a list of python dictionary to be passed
        to the 'create' method.

        Example 1: outbound with write-off:

        Account             | Debit     | Credit
        ---------------------------------------------------------
        BANK                |   900.0   |
        RECEIVABLE          |           |   1000.0
        WRITE-OFF ACCOUNT   |   100.0   |

        Example 2: internal transfer from BANK to CASH:

        Account             | Debit     | Credit
        ---------------------------------------------------------
        BANK                |           |   1000.0
        TRANSFER            |   1000.0  |
        CASH                |   1000.0  |
        TRANSFER            |           |   1000.0

        :return: A list of Python dictionary to be passed to
        env['account.move'].create.
        '''
        all_move_vals = []
        for payment in self:
            company_currency = payment.company_id.currency_id
            move_names = payment.move_name.split(
                payment._get_move_name_transfer_separator()) \
                if payment.move_name else None

            # Compute amounts.
            write_off_amount = \
                payment.payment_difference_handling == 'reconcile' and \
                -payment.payment_difference or 0.0
            if payment.payment_type in ('outbound', 'transfer'):
                counterpart_amount = payment.amount
                liquidity_line_account = \
                    payment.journal_id.default_debit_account_id
            else:
                counterpart_amount = -payment.amount
                liquidity_line_account = \
                    payment.journal_id.default_credit_account_id

            # Manage currency.
            if payment.currency_id == company_currency:
                # Single-currency.
                balance = counterpart_amount
                write_off_balance = write_off_amount
                counterpart_amount = write_off_amount = 0.0
                currency_id = False
            else:
                # Multi-currencies.
                balance = payment.currency_id._convert(
                    counterpart_amount, company_currency,
                    payment.company_id, payment.payment_date)
                write_off_balance = \
                    payment.currency_id._convert(
                        write_off_amount, company_currency,
                        payment.company_id, payment.payment_date)
                currency_id = payment.currency_id.id

            # Manage custom currency on journal for liquidity line.
            if payment.journal_id.currency_id and payment.currency_id != \
                    payment.journal_id.currency_id:
                # Custom currency on journal.
                if payment.journal_id.currency_id == company_currency:
                    # Single-currency
                    liquidity_line_currency_id = False
                else:
                    liquidity_line_currency_id = \
                        payment.journal_id.currency_id.id
                liquidity_amount = company_currency._convert(
                    balance, payment.journal_id.currency_id,
                    payment.company_id, payment.payment_date)
            else:
                # Use the payment currency.
                liquidity_line_currency_id = currency_id
                liquidity_amount = counterpart_amount

            # Compute 'name' to be used in receivable/payable line.
            rec_pay_line_name = ''
            if payment.payment_type == 'transfer':
                rec_pay_line_name = payment.name
            else:
                if payment.partner_type == 'customer':
                    if payment.payment_type == 'inbound':
                        rec_pay_line_name += _("Customer Payment")
                    elif payment.payment_type == 'outbound':
                        rec_pay_line_name += _("Customer Credit Note")
                elif payment.partner_type == 'supplier':
                    if payment.payment_type == 'inbound':
                        rec_pay_line_name += _("Vendor Credit Note")
                    elif payment.payment_type == 'outbound':
                        rec_pay_line_name += _("Vendor Payment")
                if payment.invoice_ids:
                    rec_pay_line_name += \
                        ': %s' % ', '.join(payment.invoice_ids.mapped('name'))

            # Compute 'name' to be used in liquidity line.
            if payment.payment_type == 'transfer':
                liquidity_line_name = \
                    _('Transfer to %s') % payment.destination_journal_id.name
            else:
                liquidity_line_name = payment.name

            # ==== 'inbound' / 'outbound' ====

            move_vals = {
                'date': payment.payment_date,
                'ref': payment.communication,
                'journal_id': payment.journal_id.id,
                'currency_id':
                    payment.journal_id.currency_id.id or
                    payment.company_id.currency_id.id,
                'partner_id': payment.partner_id.id,
                'line_ids': [
                    # Receivable / Payable / Transfer line.
                    (0, 0, {
                        'name': rec_pay_line_name,
                        'amount_currency':
                            counterpart_amount +
                            write_off_amount if currency_id else 0.0,
                        'currency_id': currency_id,
                        'debit':
                            balance + write_off_balance > 0.0 and
                            balance + write_off_balance or 0.0,
                        'credit':
                            balance + write_off_balance < 0.0 and -balance -
                            write_off_balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id':
                            payment.partner_id.commercial_partner_id.id,
                        'account_id': payment.destination_account_id.id,
                        'payment_id': payment.id,
                    }),
                    # Liquidity line.
                    (0, 0, {
                        'name': liquidity_line_name,
                        'amount_currency': -liquidity_amount
                        if liquidity_line_currency_id else 0.0,
                        'currency_id': liquidity_line_currency_id,
                        'debit': balance < 0.0 and -balance or 0.0,
                        'credit': balance > 0.0 and balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id':
                            payment.partner_id.commercial_partner_id.id,
                        'account_id': liquidity_line_account.id,
                        'payment_id': payment.id,
                    }),
                ],
            }

            # New code added to create multiple write-off journal items in
            # payment
            company = payment.journal_id.company_id or payment.company_id
            total_write_off_amt = payment.company_id.currency_id._convert(
                sum(payment.write_off_account_ids.mapped('write_off_amount')),
                payment.currency_id, company, payment.payment_date)
            if payment.payment_difference_handling\
                    == 'reconcile' and abs(write_off_balance) != \
                    total_write_off_amt:
                raise UserError(_("Enter correct Write-Off amount."))
            if write_off_balance and payment.write_off_account_ids:
                for write_off_line in payment.write_off_account_ids:
                    if write_off_balance < 0.0:
                        write_off_line.write_off_amount = \
                            -write_off_line.write_off_amount
                    move_vals['line_ids'].append((0, 0, {
                        'name': write_off_line.write_off_label,
                        'amount_currency': -write_off_line.write_off_amount,
                        'currency_id': currency_id,
                        'debit':
                            write_off_line.write_off_amount < 0.0 and
                            -write_off_line.write_off_amount or 0.0,
                        'credit':
                            write_off_line.write_off_amount > 0.0 and
                            write_off_line.write_off_amount or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id':
                            payment.partner_id.commercial_partner_id.id,
                        'account_id': write_off_line.account_id.id,
                        'payment_id': payment.id,
                    }))

            if move_names:
                move_vals['name'] = move_names[0]

            all_move_vals.append(move_vals)

            # ==== 'transfer' ====
            if payment.payment_type == 'transfer':
                journal = payment.destination_journal_id

                # Manage custom currency on journal for liquidity line.
                if journal.currency_id and \
                        payment.currency_id != journal.currency_id:
                    # Custom currency on journal.
                    liquidity_line_currency_id = journal.currency_id.id
                    transfer_amount = \
                        company_currency._convert(
                            balance, journal.currency_id,
                            payment.company_id, payment.payment_date)
                else:
                    # Use the payment currency.
                    liquidity_line_currency_id = currency_id
                    transfer_amount = counterpart_amount

                transfer_move_vals = {
                    'date': payment.payment_date,
                    'ref': payment.communication,
                    'partner_id': payment.partner_id.id,
                    'journal_id': payment.destination_journal_id.id,
                    'line_ids': [
                        # Transfer debit line.
                        (0, 0, {
                            'name': payment.name,
                            'amount_currency': -counterpart_amount if
                            currency_id else 0.0,
                            'currency_id': currency_id,
                            'debit': balance < 0.0 and -balance or 0.0,
                            'credit': balance > 0.0 and balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id':
                                payment.partner_id.commercial_partner_id.id,
                            'account_id':
                                payment.company_id.transfer_account_id.id,
                            'payment_id': payment.id,
                        }),
                        # Liquidity credit line.
                        (0, 0, {
                            'name':
                                _('Transfer from %s') %
                                payment.journal_id.name,
                            'amount_currency': transfer_amount
                            if liquidity_line_currency_id else 0.0,
                            'currency_id': liquidity_line_currency_id,
                            'debit': balance > 0.0 and balance or 0.0,
                            'credit': balance < 0.0 and -balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id':
                                payment.partner_id.commercial_partner_id.id,
                            'account_id':
                payment.destination_journal_id.default_credit_account_id.id,
                            'payment_id': payment.id,
                        }),
                    ],
                }

                if move_names and len(move_names) == 2:
                    transfer_move_vals['name'] = move_names[1]

                all_move_vals.append(transfer_move_vals)
        return all_move_vals


class AccountPaymentWrite_off(models.Model):
    _name = "account.payment.write.off"
    _description = "Account Payment Write-Off"

    account_id = fields.Many2one('account.account', string="Account")
    write_off_label = fields.Char(string="Label")
    write_off_amount = fields.Monetary(string="Amount")
    account_payment_id = fields.Many2one('account.payment', string="Payment")
    currency_id = fields.Many2one(
        'res.currency', string='Currency')
