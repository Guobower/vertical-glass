from openerp import models, fields, api

class GlassShape(models.Model):
    _name = 'product.glass.shape'
    _description = 'Glass Shape'

    name = fields.Char('Name', required=True)
    margin = fields.Float('Margin (%)', required=True, default=0.0)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s [+ %s%%]" % (record.name, str(record.margin))))
        return result