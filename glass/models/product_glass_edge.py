from openerp import models, fields, api

class GlassEdge(models.Model):
    _name = 'product.glass.edge'
    _description = "Glass Edge"

    name = fields.Char('Name', required=True)
    price = fields.Char('Price (M)', required=True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s [%s EUR]" % (record.name, record.price)))
        return result