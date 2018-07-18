# -*- coding: utf-8 -*-
"""
Manage glass extras (suppléments - FR) and their type
"""

import logging
from openerp import api, fields, models
_logger = logging.getLogger(__name__)


class GlassExtraType(models.Model):
    """
    Types of extra
    """
    _name = 'product.glass.extra.type'
    _description = "Glass Extra Type"

    name = fields.Char(required=True)

class GlassExtras(models.Model):
    """
    Main extra class
    """
    _name = 'product.glass.extra'
    _description = "Glass Extra"

    name = fields.Char(required=True)
    type_id = fields.Many2one('product.glass.extra.type', required=True)
    price = fields.Monetary('Price /m²', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)

    @api.multi
    def name_get(self):
        """
        Custom display used in lieu of name
        """
        result = []
        for record in self:
            # If admin
            if self.env.user.id == 1:
                result.append((record.id, "%s [%.2f%s /m^2]" % (record.name, record.price, record.currency_id.symbol)))
            else:
                result.append((record.id, "%s" % (record.name)))
                
        return result
