# -*- coding: utf-8 -*-
# from odoo import http


# class SipmentTrackingModule(http.Controller):
#     @http.route('/sipment_tracking_module/sipment_tracking_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sipment_tracking_module/sipment_tracking_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sipment_tracking_module.listing', {
#             'root': '/sipment_tracking_module/sipment_tracking_module',
#             'objects': http.request.env['sipment_tracking_module.sipment_tracking_module'].search([]),
#         })

#     @http.route('/sipment_tracking_module/sipment_tracking_module/objects/<model("sipment_tracking_module.sipment_tracking_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sipment_tracking_module.object', {
#             'object': obj
#         })
