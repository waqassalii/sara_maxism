# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPdf(http.Controller):
#     @http.route('/custom_pdf/custom_pdf/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_pdf/custom_pdf/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_pdf.listing', {
#             'root': '/custom_pdf/custom_pdf',
#             'objects': http.request.env['custom_pdf.custom_pdf'].search([]),
#         })

#     @http.route('/custom_pdf/custom_pdf/objects/<model("custom_pdf.custom_pdf"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_pdf.object', {
#             'object': obj
#         })
