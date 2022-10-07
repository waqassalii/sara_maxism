# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RepairOrder(models.Model):

    _inherit = 'repair.order'

    # fault_note = fields.Html()
    fault_note = fields.Text()
    performed_services = fields.Text()
    further_actions = fields.Text()

