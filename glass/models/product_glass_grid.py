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
    colour = fields.Char(required=True)
    sockets = fields.Integer(required=True, default=0)
    price = fields.Float('Price / socket', required=True)

    @api.multi
    def name_get(self):
        """
        Custom display used in lieu of name
        """
        result = []
        for record in self:
            result.append((record.id, "%s %d sockets (%s) [%.2f EUR]"
                           % (record.name, record.sockets, record.colour, record.price)))
        return result

    @api.multi
    def compute_price(self):
        return self.price * self.sockets
