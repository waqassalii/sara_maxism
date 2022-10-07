# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models,fields,_
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    user_id = fields.Many2one('res.users', string='Salesperson')

    def create_custom_delivery_order(self):
        if self:
            if self.delivery_count:
                raise ValidationError('Delivery order already exists')

        self._action_confirm()

    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        # self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True

class AccountMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_code = fields.Char(related='product_id.default_code')
