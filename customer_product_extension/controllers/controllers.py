# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerProductExtension(http.Controller):
#     @http.route('/customer_product_extension/customer_product_extension/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_product_extension/customer_product_extension/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_product_extension.listing', {
#             'root': '/customer_product_extension/customer_product_extension',
#             'objects': http.request.env['customer_product_extension.customer_product_extension'].search([]),
#         })

#     @http.route('/customer_product_extension/customer_product_extension/objects/<model("customer_product_extension.customer_product_extension"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_product_extension.object', {
#             'object': obj
#         })
