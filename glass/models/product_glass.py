# -*- coding: utf-8 -*-
"""
Define a glass product by extending the product class.
Only constraint with max rate value will be applied
"""

import logging
from openerp import models, fields, api, _
_logger = logging.getLogger(__name__)


class ProductGlass(models.Model):
    _inherit = 'product.product'

    minimum_invoiceable = fields.Float('Minimum Invoiceable (m^2)', default=1)
    order_line_id = fields.Many2one('sale.order.line', 'Order Line')
    order_reference = fields.Char('Order reference')
    price_with_auto_margin = fields.Float('Marged Price', compute='_compute_price_with_auto_margin')
    maximum_area_possible = fields.Float('Maximum Area with warranty (m^2)', default='3')
    maximum_area_substitute = fields.Many2one('product.product', string='Substitute product')

    @api.multi
    @api.depends('categ_id')
    def _compute_price_with_auto_margin(self):
        for product in self:
            product.price_with_auto_margin = product.lst_price * product.categ_id.margin_default

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search((args + ['|', ('name', 'ilike', name), '|',
                                        ('attribute_value_ids', 'ilike', name),
                                        ('default_code', 'ilike', name)]), limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()
