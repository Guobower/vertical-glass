# -*- coding: utf-8 -*-
"""
Manage dimension constraints (contrainte de taill - FR)
Only constraint with max rate value will be applied
"""

import logging
from openerp import api, fields, models
_logger = logging.getLogger(__name__)


class GlassDimConstraint(models.Model):
    """
    Main dimension constraint class
    """
    _name = 'product.glass.dimconstraint'
    _description = "Glass Dimension Constraint"
    _order = "rate asc"

    name = fields.Char(required=True)
    mode = fields.Selection([('inside_rectangle', 'Inside rectangle'), ('area', 'Area')], required=True)
    width = fields.Integer('Width (mm)', default=1000)
    height = fields.Integer('Height (mm)', default=1000)
    area = fields.Float('Area (m^2)', default=1)
    rate = fields.Integer('Rate (%)', required=True)

    @api.multi
    def name_get(self):
        """
        Custom display used in lieu of name
        """
        result = []
        for record in self:
            # If Admin
            if self.env.user.id == 1:
                result.append((record.id, "%s [+%s %%]" % (record.name, record.rate)))
            else:
                result.append((record.id, "%s" % (record.name)))
        return result
