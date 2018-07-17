{
    'name': "Glass Company in Odoo",
    'version': '9.0.1.0.3',
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Sale',
    'depends': [
        'sale',
    ],
    'data': [
        'views/settings_view.xml',
        'views/res_config.xml',
        'views/product_category_view.xml',
        'views/product_glass_finish_view.xml',
        'views/product_glass_edge_view.xml',
        'views/product_glass_grid_view.xml',
        'views/product_glass_spacer_view.xml',
        'views/product_glass_extras_view.xml',
        'views/product_glass_shape_view.xml',
        'views/product_glass_finish_view.xml',
        'views/product_glass_dimconstraint_view.xml',
        'views/res_partner_view.xml',
        'views/product_template.xml',
        'views/sale_order_view.xml',
        'views/sale_order_line_view.xml',

        'data/product_category_data.xml',
        'data/glass_company_setting.xml',
        'data/report_paper_format.xml',

        'reports/report_footer.xml',
        'reports/sale_order_report_customer.xml',
        'reports/sale_order_report_technical.xml',
        'reports/sale_order_report_full.xml',

        'security/ir.model.access.csv',
    ],
    'demo': [
        'data/product_product_demo.xml',
    ],
}