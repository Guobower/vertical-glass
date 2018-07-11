# -*- coding: utf-8 -*-
"""
Manage spacer (intercalaire - FR) with price by volume(m3) and colour
"""

import logging
from openerp import api, fields, models
_logger = logging.getLogger(__name__)


class GlassSpacer(models.Model):
    """
    Main spacer class
    """
    _name = 'product.glass.spacer'
    _description = "Glass Spacer"

    name = fields.Char(required=True)
    colour = fields.Char(required=True)
    price = fields.Float('Price / m^2', required=True)

    @api.multi
    def name_get(self):
        """
        Custom display used in lieu of name
        """
        result = []
        for record in self:
            result.append((record.id, "%s (%s) [%.2f EUR]"
                           % (record.name, record.colour, record.price)))
        return result

    @api.multi
    def compute_price(self, volume_in_cube_meters):
        return self.price * volume_in_cube_meters