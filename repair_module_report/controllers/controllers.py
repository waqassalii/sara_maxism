# -*- coding: utf-8 -*-
# from odoo import http


# class RepairModuleReport(http.Controller):
#     @http.route('/repair_module_report/repair_module_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/repair_module_report/repair_module_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('repair_module_report.listing', {
#             'root': '/repair_module_report/repair_module_report',
#             'objects': http.request.env['repair_module_report.repair_module_report'].search([]),
#         })

#     @http.route('/repair_module_report/repair_module_report/objects/<model("repair_module_report.repair_module_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('repair_module_report.object', {
#             'object': obj
#         })
