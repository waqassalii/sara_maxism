# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=1, default=lambda self: self.env.user,
        domain=[])
