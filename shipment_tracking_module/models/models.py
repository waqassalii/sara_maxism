# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    shipment_charges = fields.Float('Shipment Charges')
    tracking_ref = fields.Char('Tracking Reference')
