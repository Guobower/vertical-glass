# -*- coding: utf-8 -*-
import logging
from openerp import api, fields, models
_logger = logging.getLogger(__name__)


class GlassBraces(models.Model):
    """
    Manage braces (croisillon - FR) with price per socket (alvéoles -FR)
    """
    _name = 'product.glass.braces'
    _description = "Glass Braces"

    name = fields.Char(required=True)
    price = fields.Char('Price / socket', required=True)

    @api.multi
    def name_get(self):
        """
        Custom name display format
        """
        result = []
        for record in self:
            result.append((record.id, "%s [%s EUR]" % (record.name, record.price)))
        return result
