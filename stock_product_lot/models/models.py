# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    asset_tag = fields.Char()
    installation_date = fields.Date()
    warranty_expiration = fields.Date()
    pm_on_date = fields.Date('PM On Date')
    pm_due_date = fields.Date('PM Due Date')

class Repair(models.Model):
    _inherit = 'repair.order'
    guarantee_limit = fields.Date(related='lot_id.warranty_expiration')
    asset_tag = fields.Char(related='lot_id.asset_tag')
    installation_date = fields.Date(related='lot_id.installation_date')
    pm_on_date = fields.Date()
    pm_due_date = fields.Date()

    # @api.onchange('lot_id')
    # def onchange_lot_id(self):
    #     self.pm_on_date = self.lot_id.pm_on_date
    #     self.pm_due_date = self.lot_id.pm_due_date

    @api.onchange('pm_on_date','pm_due_date')
    def onchange_pm_dates(self):
        self.lot_id.pm_on_date = self.pm_on_date
        self.lot_id.pm_due_date = self.pm_due_date