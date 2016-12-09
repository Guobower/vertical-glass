{
    'name': "Glass Company in Odoo",
    'version': '9.0.1.0.1',
    'depends': [
	   'sale',
    ],
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Sale',
    'description': 
    """
    
    
    This module has been developed by AbAKUS it-solutions
    """,
    'data': [
        'views/res_config.xml',
        'views/settings_view.xml',
        'views/product_category_view.xml',
        'views/product_glass_shape_view.xml',
        'views/product_glass_edge_view.xml',
        'views/res_partner_view.xml',
        'views/product_glass_view.xml',
        'views/sale_order_view.xml',
        'views/sale_order_line_view.xml',

        'data/product_category_data.xml',
        'data/glass_company_setting.xml',
        ],
}