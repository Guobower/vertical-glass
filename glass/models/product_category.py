# -*- coding: utf-8 -*-
"""
Product category
"""

import logging
from openerp import api, fields, models
_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    """
    Additional element to be inherited by glass product
    """
    _inherit = 'product.category'

    margin_default = fields.Float('Default Margin', default=1)
    min_invoice_area = fields.Integer(string="Min. Invoiceable Area [m^2]")
    linked_product_ids = fields.One2many('product.product', 'categ_id', string="Linked Product")

