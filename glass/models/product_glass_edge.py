# -*- coding: utf-8 -*-
"""
Manage edges (bords - FR) with price per socket (alvéoles -FR)
"""

import logging
from openerp import models, fields, api
_logger = logging.getLogger(__name__)


class GlassEdge(models.Model):
    """
    Main edges class
    price per meter of border
    """
    _name = 'product.glass.edge'
    _description = "Glass Edge"

    name = fields.Char(required=True)
    price = fields.Char('Price (M)', required=True)

    @api.multi
    def name_get(self):
        """
        custom display name
        """
        result = []
        for record in self:
            result.append((record.id, "%s [%s EUR]" % (record.name, record.price)))
        return result
