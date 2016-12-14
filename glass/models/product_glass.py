from openerp import models, fields, api, _


import logging
_logger = logging.getLogger(__name__)

class ProductGlass(models.Model):
    _inherit = 'product.product'

    minimum_invoicable = fields.Float('Minimum Invoicable (m^2)', default=1)
    order_line_id = fields.Many2one('sale.order.line', 'Order Line')
    order_reference = fields.Char('Order reference')
    price_with_auto_margin = fields.Float('Marged Price', compute='_compute_price_with_auto_margin')