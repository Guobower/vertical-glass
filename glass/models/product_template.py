# -*- coding: utf-8 -*-
"""
Extension of product.template in order to add a list of extras
"""
import logging
from openerp import models, fields, api
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    """ Main class holding additional fields.
    """
    _inherit = 'product.template'

    maximum_area_possible = fields.Float('Maximum Area with warranty (m^2)', default='3')
    maximum_area_substitute = fields.Many2one('product.product', string='Substitute product')
    minimum_invoiceable = fields.Float('Minimum Invoiceable (m^2)', default=1)

    # Glass product presets
    glass_back_id = fields.Many2one('product.product', string="Glass (back)")
    glass_middle_id = fields.Many2one('product.product', string="Glass (middle)")
    product_extras_ids = fields.Many2many('product.glass.extra', string='Product extras')

    # Price
    margin = fields.Float('Margin', default=1)
    price_with_auto_margin = fields.Float('Marged Price', compute='_compute_sale_price')

    # keep a reference of the order in this line
    order_reference = fields.Char()
    
    @api.multi
    @api.onchange('margin', 'standard_price')
    def _compute_sale_price(self):
        for product in self:
            product.price_with_auto_margin = product.standard_price * product.margin
            product.list_price = product.standard_price * product.margin
