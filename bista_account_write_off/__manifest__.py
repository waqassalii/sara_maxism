# -*- encoding: utf-8 -*-
##############################################################################
#
#    Bista Solutions Pvt. Ltd
#    Copyright (C) 2019 (http://www.bistasolutions.com)
#
##############################################################################
{
    'name': 'Account Multiple Write-Off Lines (Odoo Enterprise)',
    'version': '13.0.0.0.1',
    'summary': 'Allow multiple write off account entry - For Odoo Enterprise',
    'author': "Bista Solutions",
    'website': "http://www.bistasolutions.com",
    'description': """
Write-Off account management
============================
This module allows you to easily add extra account as many as you want in
write off journal entry. it will add extra lines in existing entry
    """,
    'depends': ['account_accountant'],
    'category': 'Accounting',
    'price': 25,
    'currency': 'USD',
    'license': 'OPL-1',
    'data': [
        'security/ir.model.access.csv',
        'views/payment_write_off.xml',
    ],
    'images':['static/description/cover.png','static/description/icon.png'],
    'installable': True,
    'application': False
}

