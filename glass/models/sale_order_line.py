from openerp import models, fields, api

class sale_order_line(models.Model):
    _inherit = ['sale.order.line']
