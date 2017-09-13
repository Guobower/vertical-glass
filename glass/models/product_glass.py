from openerp import models, fields, api, _


import logging
_logger = logging.getLogger(__name__)

class ProductGlass(models.Model):
    _inherit = 'product.product'

    minimum_invoicable = fields.Float('Minimum Invoicable (m^2)', default=1)
    order_line_id = fields.Many2one('sale.order.line', 'Order Line')
    order_reference = fields.Char('Order reference')
    price_with_auto_margin = fields.Float('Marged Price', compute='_compute_price_with_auto_margin')
    maximum_area_possible = fields.Float('Maximum Area with warranty (m^2)', default='3')
    maximum_area_substitute = fields.Many2one('product.product', 'Substitude product')

    @api.multi
    @api.depends('categ_id', 'lst_price')
    def _compute_price_with_auto_margin(self):
        for product in self:
            product.price_with_auto_margin = product.lst_price * (1 + product.categ_id.margin / 100)


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search((args + ['|', ('name', 'ilike', name), '|', ('attribute_value_ids', 'ilike', name), ('default_code', 'ilike', name)]), limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()     