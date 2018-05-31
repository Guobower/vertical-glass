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
    price = fields.Float('Price (m^2)', required=True, default=1)

    @api.multi
    def name_get(self):
        """ Custom naming """
        result = []
        for record in self:
            result.append((record.id, "%s [x %s]" % (record.name, str(record.price))))
        return result

    @api.multi
    def compute_price(self, volume_in_cube_meters):
        """ Custom price computation """
        return self.price * volume_in_cube_meters
