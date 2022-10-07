# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseDeliveryReports(http.Controller):
#     @http.route('/purchase_delivery_reports/purchase_delivery_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_delivery_reports/purchase_delivery_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_delivery_reports.listing', {
#             'root': '/purchase_delivery_reports/purchase_delivery_reports',
#             'objects': http.request.env['purchase_delivery_reports.purchase_delivery_reports'].search([]),
#         })

#     @http.route('/purchase_delivery_reports/purchase_delivery_reports/objects/<model("purchase_delivery_reports.purchase_delivery_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_delivery_reports.object', {
#             'object': obj
#         })
