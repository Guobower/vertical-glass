from openerp import models, fields, api, _

class ProductGlass(models.Model):
    _inherit = 'product.product'

    minimum_invoicable = fields.Float('Minimum Invoicable (m^2)', default=1)
    order_line_id = fields.Many2one('sale.order.line', 'Order Line')
    order_reference = fields.Char('Order reference')
    price_with_auto_margin = fields.Float('Marged Price', compute='_compute_price_with_auto_margin')

    @api.multi
    @api.depends('categ_id')
    def _compute_price_with_auto_margin(self):
        for product in self:
            product.price_with_auto_margin = product.lst_price * product.categ_id.margin_default
