from openerp import models, fields, api

class ProductGlass(models.Model):
    _inherit = 'product.product'

    minimum_invoicable = fields.Float('Minimum Invoicable (m^2)', default=1)
