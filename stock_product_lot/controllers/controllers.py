# -*- coding: utf-8 -*-
# from odoo import http


# class StockProductLot(http.Controller):
#     @http.route('/stock_product_lot/stock_product_lot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_product_lot/stock_product_lot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_product_lot.listing', {
#             'root': '/stock_product_lot/stock_product_lot',
#             'objects': http.request.env['stock_product_lot.stock_product_lot'].search([]),
#         })

#     @http.route('/stock_product_lot/stock_product_lot/objects/<model("stock_product_lot.stock_product_lot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_product_lot.object', {
#             'object': obj
#         })
