# -*- encoding: utf-8 -*-

from openerp import models, fields, api


class ProductTemplate(models.Model):
    """
    Extension of product.template in order to add a list of extras
    """
    _inherit = 'product.template'

    product_extras_ids = fields.Many2many('product.glass.extra', string='Product extras')
