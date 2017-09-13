from openerp import models, fields, api

class GlassFinish(models.Model):
    _name = 'product.glass.finish'
    _description = 'Glass Finish'

    name = fields.Char('Name', required=True)
    price = fields.Float('Price (m^2)', required=True, default=1)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s [%s EUR]" % (record.name, str(record.price))))
        return result