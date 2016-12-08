from openerp import models, fields, api

class SaleOrderLineSub(models.Model):
    _name = 'sale.order.line.sub'
    _description = 'Sub Order Line Shape'

    glass_id = fields.Many2one('product.product', 'Product', required=True)

    width = fields.Float('Width (mm)', default=100)
    height = fields.Float('Height (mm)', default=100)
    
