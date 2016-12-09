from openerp import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # name
    name = fields.Char('Name')
    description_structured = fields.Text('Line structured description')
    sale_order_line_sub_ids = fields.One2many('sale.order.line.sub', 'order_line_id', 'Sub Order Lines')
    sub_lines_total = fields.Float('Lines Total', compute='_compute_sub_lines_total', store=True)

    installation = fields.Boolean('Installation', default=False)
    installation_qty = fields.Float('Installation Quantity', default=1)
    installation_total = fields.Float('Installation Total', compute='_compute_totals')

    moving = fields.Boolean('Moving', default=False)
    moving_qty = fields.Float('Moving Quantity')
    moving_total = fields.Float('Moving Total', compute='_compute_totals')

    km_qty = fields.Float('KM Quantity')
    km_total = fields.Float('KM Total', compute='_compute_totals')

    price_unit = fields.Float('Price', compute='_compute_totals')
    margin_applied = fields.Float('Applied margin')
    # price_total

    @api.depends('sale_order_line_sub_ids')
    def _compute_sub_lines_total(self):
        for line in self:
            t = 0
            for sub_line in line.sale_order_line_sub_ids:
                t = t + sub_line.total
            line.sub_lines_total = t

    @api.model
    @api.depends('installation', 'installation_qty', 'moving', 'moving_total', 'km_qty', 'sub_lines_total')
    def _compute_totals(self):
        setting = self.env['glass.sale.config.settings.data'].search([])
        if len(setting) > 1:
            setting = setting[0]

        for line in self:
            # installation total
            if line.installation:
                line.installation_total = line.installation_qty * setting.installation_price
            else:
                line.installation_total = 0

            # moving total
            if line.moving:
                line.moving_total = line.moving_qty * setting.moving_price
            else:
                line.moving_total = 0

            # KM total
            line.km_total = line.km_qty * setting.km_price

            # total without margin
            line.price_unit = line.sub_lines_total + line.installation_total + line.moving_total + line.km_total

            # total with margin
            line.pric_total = line.price_unit * line.margin_applied
