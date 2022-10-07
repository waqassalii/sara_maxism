# -*- coding: utf-8 -*-

from odoo import models, api

class AccountReport(models.AbstractModel):
    _inherit = 'account.report'

    @api.model
    def _query_get(self, options, domain=None):
        domain = self._get_options_domain(options) + (domain or [])
        users = self.env.ref('account.group_account_manager').sudo().users.ids
        if self.env.user.id not in users:
            domain.append(('move_id.user_id', '=', self.env.user.id))
        self.env['account.move.line'].check_access_rights('read')

        query = self.env['account.move.line']._where_calc(domain)

        # Wrap the query with 'company_id IN (...)' to avoid bypassing company access rights.
        self.env['account.move.line']._apply_ir_rules(query)

        return query.get_sql()
