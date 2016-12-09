from openerp import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # name
    description_structured = fields.Text('Line structured description')
    sale_order_line_sub_ids = fields.One2many('sale.order.line.sub', 'order_line_id', 'Sub Order Lines')

    installation = fields.Boolean('Installation', default=False)
    installation_qty = fields.Float('Installation Quantity')
    installation_total = fields.Float('Installation Total')

    moving = fields.Boolean('Moving', default=False)
    moving_qty = fields.Float('Moving Quantity')
    moving_total = fields.Float('Moving Total')

    km_qty = fields.Float('KM Quantity')
    km_total = fields.Float('KM Total')

    # price_unit
    margin_applied = fields.Float('Applied margin')
    # price total
