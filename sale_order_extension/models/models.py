# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery = fields.Char()
    end_user = fields.Many2one('res.partner')
    order_class = fields.Selection([('A','A'),
                                    ('B','B'),
                                    ('C','C'),
                                    ('D','D')],string='Class')
    delivery_term = fields.Many2one('account.incoterms')
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=1, default=lambda self: self.env.user,
        domain=[])

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        invoice_vals = {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.pricelist_id.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'user_id': self.user_id.id,
            'invoice_user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(self.partner_invoice_id.id)).id,
            'partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'payment_reference': self.reference,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
            'end_user': self.end_user.id if self.end_user else False,
        }
        return invoice_vals

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_code = fields.Char('Product Code', related='product_id.default_code')

    @api.depends('product_id', 'order_id.state', 'qty_invoiced', 'qty_delivered')
    def _compute_product_updatable(self):
        for line in self:
            if line.state in ['done', 'cancel'] or (
                    line.state == 'sale' and (line.qty_invoiced > 0 or line.qty_delivered > 0)):
                line.product_updatable = False
            else:
                line.product_updatable = True
            if line.product_id:
                line.name = line.product_id.name