from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    name = fields.Char('Name')
    description_structured = fields.Text('Line structured description', compute="_compute_description", store=True)
    sale_order_line_sub_ids = fields.One2many('sale.order.line.sub', 'order_line_id', 'Sub Order Lines')
    sub_lines_total = fields.Float('Lines Total', compute='_compute_sub_lines_total', store=True)

    installation = fields.Boolean('Installation', default=False)
    installation_qty = fields.Float('Installation Quantity', default=1)
    installation_total = fields.Float('Installation Total', compute='_compute_totals')

    moving = fields.Boolean('Moving', default=False)
    moving_qty = fields.Float('Moving Quantity', default=1)
    moving_total = fields.Float('Moving Total', compute='_compute_totals')

    km = fields.Boolean('KM', default=True)
    km_qty = fields.Float('KM Quantity')
    km_total = fields.Float('KM Total', compute='_compute_totals')

    miscellaneous_total = fields.Float('Miscelaneous', default=0)

    price_tmp = fields.Float('Base price', compute='_compute_totals', store=True)
    price_unit = fields.Float('Price', compute='_compute_totals', store=True)
    margin_applied = fields.Float('Applied margin', default=1.0)

    @api.model
    def get_taxes(self):
        setting = self.env['account.config.settings'].search([('company_id', '=', self.env.user.company_id.id)])
        if len(setting) > 1:
            setting = setting[0]
        return [(6, 0, [setting.sale_tax_id.id])]

    tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)], default=get_taxes)

    @api.multi
    @api.depends('sale_order_line_sub_ids')
    def _compute_description(self):
        for line in self:
            text = ''
            for sub in line.sale_order_line_sub_ids:
                text = text + str(sub.description.encode('utf-8')) + '\n'
            line.description_structured = text

    @api.multi
    @api.depends('sale_order_line_sub_ids')
    def _compute_sub_lines_total(self):
        for line in self:
            t = 0
            for sub_line in line.sale_order_line_sub_ids:
                t = t + sub_line.total
            line.sub_lines_total = t

    @api.multi
    @api.depends('installation', 'installation_qty', 'moving', 'moving_qty', 'moving_total', 'km', 'km_qty', 'sub_lines_total', 'margin_applied', 'miscellaneous_total')
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
            if line.km:
                line.km_total = line.km_qty * setting.km_price
            else:
                line.km_total = 0

            # total without margin
            line.price_tmp = line.sub_lines_total + line.installation_total + line.moving_total + line.km_total + line.miscellaneous_total

            # total with margin
            line.price_unit = line.price_tmp * line.margin_applied

    @api.model
    def create(self, values):
        if 'product_id' not in values:
            product_id = self.env['product.product'].create({
                    'name': values['name'],
                    'type': 'product',
                    'sale_ok': False,
                    'purchase_ok': False,
                    'order_reference': self.order_id.name,
                })
            values['product_id'] = product_id.id
        return super(SaleOrderLine, self).create(values)

    @api.multi
    def write(self, values):
        for line in self:
            if not line.product_id:
                product_id = self.env['product.product'].create({
                        'name': line.name,
                        'type': 'product',
                        'sale_ok': False,
                        'purchase_ok': False,
                        'order_reference': line.order_id.name,
                        'order_line_id': line.id,
                    })
                line.product_id = produdtc_id.id
            else:
                line.product_id.name = line.name
                line.product_id.order_line_id = line.id
        return super(SaleOrderLine, self).write(values)      
