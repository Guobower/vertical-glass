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

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s" % record.name))
        return result


class GlassExtras(models.Model):
    """
    Main extra class
    """
    _name = 'product.glass.extra'
    _description = "Glass Extra"

    name = fields.Char(required=True)
    type_id = fields.Many2one('product.glass.extra.type', required=True)
    price = fields.Char('Price', required=True)

    @api.multi
    def name_get(self):
        """
        Custom display used in lieu of name
        """
        result = []
        for record in self:
            result.append((record.id, "%s [%s EUR]" % (record.name, record.price)))
        return result
