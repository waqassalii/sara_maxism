{
    'name': 'Annexure Report C',
    'version': '14.0.2.1.0',
    'sequence': 10,
    'category': '',
    'author': 'AnaConEx Solutions',
    'license': 'AGPL-3',
    'depends': [
        'mail',
        'account',
        'report_xlsx',
    ],
    'data': [
        'wizards/wiz_form_dates_report.xml',
        'views/account_annexure.xml',
        'security/ir.model.access.csv',
        'reports/excel_report.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
