# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    country_origin = fields.Many2one('res.country',string="Country of Origin")
    manufacturer = fields.Many2one('res.partner')
    registration_no = fields.Char('Registration No.')
    registration_status = fields.Selection([
        ('registered', 'Registered'),
        ('dossier_submitted', 'Dossier Submitted'),
        ('under_process', 'Under Process'),
        ('not_required', 'Not Required'),
    ], string="Registration")

    order_class = fields.Selection([('A', 'A'),
                                    ('B', 'B'),
                                    ('C', 'C'),
                                    ('D', 'D')], string='Class')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    fax_number = fields.Char()
    strn_number = fields.Char('STRN Number')
    fax = fields.Char()
    department_char = fields.Char('Department')