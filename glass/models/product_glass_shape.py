from openerp import models, fields, api

class GlassShape(models.Model):
    _name = 'product.glass.shape'
    _description = 'Glass Shape'

    name = fields.Char('Name', required=True)
    multiplier = fields.Float('Multiplier', required=True, default=1)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s [x %s]" % (record.name, record.multiplier)))
        return result