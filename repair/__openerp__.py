# -*- coding: utf-8 -*-

{
    'name': "Glass Repair Management",
    'version': '9.0.1.0.0',
    'depends': [
        'glass',
        'account'
    ],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Account',
    'description': """
This module has been developed by Valentin Thirion @ AbAKUS it-solutions""",
    'data': [
        'views/repair_order_view.xml',
        'views/account_invoice_view.xml',
        'security/ir.model.access.csv',
        'data/repair_security.xml',
    ],
}