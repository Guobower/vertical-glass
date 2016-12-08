from openerp import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reference_auto = fields.Char('Reference auto')
    header_text = fields.Text('Header text')
    footer_text = fields.Text('Footer text')