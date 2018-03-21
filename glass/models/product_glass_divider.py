# -*- coding: utf-8 -*-
"""
Manage divider (intercalaire - FR) with price by volume(m3) and colour
"""

import logging
from openerp import api, fields, models
_logger = logging.getLogger(__name__)


class GlassDivider(models.Model):
    """
    Main divider class
    """
    _name = 'product.glass.divider'
    _description = "Glass Divider"

    name = fields.Char(required=True)
    colour = fields.Char(required=True)
    price = fields.Char('Price / m3', required=True)

    @api.multi
    def name_get(self):
        """
        Custom display used in lieu of name
        """
        result = []
        for record in self:
            result.append((record.id, "%s (%s) [%s EUR]" % (record.name, record.colour, record.price)))
        return result
