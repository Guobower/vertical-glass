from openerp import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    description_structured = fields.Text('Line structured description')

    installation = fields.Boolean('Installation', default=False)
    installation_qty = fields.Float('Installation Quantity')
    installation_total = fields.Float('Installation Total')

    moving = fields.Boolean('Moving', default=False)
    moving_qty = fields.Float('Moving Quantity')
    moving_total = fields.Float('Moving Total')

    km_qty = fields.Float('KM Quantity')
    km_total = fields.Float('KM Total')

    margin_applied = fields.Float('Applied margin')
