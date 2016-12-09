from openerp import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # name
    name = fields.Char('Name')
    description_structured = fields.Text('Line structured description')
    sale_order_line_sub_ids = fields.One2many('sale.order.line.sub', 'order_line_id', 'Sub Order Lines')
    sub_lines_total = fields.Float('Lines Total', compute='_compute_sub_lines_total', store=True)

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
    # price_total

    @api.depends('sub_lines_total')
    def _compute_sub_lines_total(self):
        for line in self:
            t = 0
            for sub_line in line.sale_order_line_sub_ids:
                t = t + sub_line.total
            line.sub_lines_total = t
