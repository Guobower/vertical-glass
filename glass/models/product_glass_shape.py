from openerp import models, fields, api

class GlassShape(models.Model):
    _name = 'product.glass.shape'
    _description = 'Glass Shape'

    name = fields.Char('Name', required=True)
    multiplier = fields.Float('Multiplier', required=True, default=1)    
