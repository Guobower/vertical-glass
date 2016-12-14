from openerp import models, fields, api, _

class ProductGlass(models.Model):
    _inherit = 'product.product'

    minimum_invoicable = fields.Float('Minimum Invoicable (m^2)', default=1)
    order_line_id = fields.Many2one('sale.order.line', 'Order Line')
    order_reference = fields.Char('Order reference')
