from openerp import models, fields, api

class GlassEdge(models.Model):
    _name = 'product.glass.edge'
    _description = "Glass Edge"

    name = fields.Char('Name', required=True)
    price = fields.Char('Price (M)', required=True)
