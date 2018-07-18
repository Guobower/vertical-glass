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
    price = fields.Monetary('Price /m', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)

    @api.multi
    def name_get(self):
        """
        custom display name
        """
        result = []
        for record in self:
            # If admin
            if self.env.user.id == 1:
                result.append((record.id, "%s [%.2f%s /m]" % (record.name, record.price, record.currency_id.symbol)))
            else:
                result.append((record.id, "%s" % (record.name)))
        return result
