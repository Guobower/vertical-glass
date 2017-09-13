from openerp import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    margin = fields.Float('Margin (%)', default=0)
