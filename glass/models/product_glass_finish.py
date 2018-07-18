# -*- coding: utf-8 -*-
"""
Manage glass finishes (finition - FR)
"""
from openerp import models, fields, api


class GlassFinish(models.Model):
    """
    Main class
    """
    _name = 'product.glass.finish'
    _description = 'Glass Finish'

    name = fields.Char(required=True)
    price = fields.Monetary('Price /m²', required=True, default=1)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)

    @api.multi
    def name_get(self):
        """ Custom naming """
        result = []
        for record in self:
            # If admin
            if self.env.user.id == 1:
                result.append((record.id, "%s [%.2f%s /m^2]" % (record.name, record.price, record.currency_id.symbol)))
            else:
                result.append((record.id, "%s" % (record.name)))
        return result

    @api.multi
    def compute_price(self, volume_in_cube_meters):
        """ Custom price computation """
        return self.price * volume_in_cube_meters
