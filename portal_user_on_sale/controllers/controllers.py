# -*- coding: utf-8 -*-
# from odoo import http


# class PortalUserOnSale(http.Controller):
#     @http.route('/portal_user_on_sale/portal_user_on_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/portal_user_on_sale/portal_user_on_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('portal_user_on_sale.listing', {
#             'root': '/portal_user_on_sale/portal_user_on_sale',
#             'objects': http.request.env['portal_user_on_sale.portal_user_on_sale'].search([]),
#         })

#     @http.route('/portal_user_on_sale/portal_user_on_sale/objects/<model("portal_user_on_sale.portal_user_on_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('portal_user_on_sale.object', {
#             'object': obj
#         })
