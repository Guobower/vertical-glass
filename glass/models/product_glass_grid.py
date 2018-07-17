# -*- coding: utf-8 -*-
"""
Manage internal grids (croisillons - FR) with price per socket (alvéoles -FR)
"""

import logging
from openerp import api, fields, models
_logger = logging.getLogger(__name__)


class GlassGrid(models.Model):
    """
    Main grid class
    """
    _name = 'product.glass.grid'
    _description = "Glass Grid"

    name = fields.Char(required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary('Price / socket', required=True)

    @api.multi
    def name_get(self):
        """
        Custom display used in lieu of name
        """
        result = []
        for record in self:
            result.append((record.id, "%s [%.2f %s / alv.]"
                           % (record.name, record.price, record.currency_id.symbol)))
        return result
