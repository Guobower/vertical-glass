from openerp import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    margin_default = fields.Float('Default Margin', default=1)
