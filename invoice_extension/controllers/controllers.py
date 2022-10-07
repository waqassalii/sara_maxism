# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceExtension(http.Controller):
#     @http.route('/invoice_extension/invoice_extension/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_extension/invoice_extension/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_extension.listing', {
#             'root': '/invoice_extension/invoice_extension',
#             'objects': http.request.env['invoice_extension.invoice_extension'].search([]),
#         })

#     @http.route('/invoice_extension/invoice_extension/objects/<model("invoice_extension.invoice_extension"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_extension.object', {
#             'object': obj
#         })
