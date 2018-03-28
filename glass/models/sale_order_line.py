# -*- coding: utf-8 -*-
"""
Sale order line extension
"""

import logging
from openerp import models, fields, api
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    """
    Main class adding workforce and sale_order_line_sub concepts
    """
    _inherit = 'sale.order.line'

    name = fields.Char('Name', required=True)
    description_structured = fields.Text('Line structured description', compute="_compute_description", store=True)
    sale_order_line_sub_ids = fields.One2many('sale.order.line.sub', 'order_line_id', 'Sub Order Lines')
    sub_lines_total = fields.Float('Lines Total', compute='_compute_sub_lines_total', store=True)

    men = fields.Boolean('Men quantity', default=True)
    men_quantity = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], 'Men quantity', default='1')

    installation = fields.Boolean('Installation', default=False)
    installation_qty = fields.Float('Installation Quantity', default=1)
    installation_total = fields.Float('Installation Total', compute='_compute_totals')

    moving = fields.Boolean('Moving', default=False)
    moving_qty = fields.Float('Moving Quantity', default=1)
    moving_total = fields.Float('Moving Total', compute='_compute_totals')

    km = fields.Boolean('KM', default=True)
    km_qty = fields.Float('KM Quantity', default=40)
    km_total = fields.Float('KM Total', compute='_compute_totals')

    miscellaneous_total = fields.Float('Miscelaneous', default=0)

    price_tmp = fields.Float('Base price', compute='_compute_totals', store=True)
    price_unit = fields.Float('Price', compute='_compute_totals', store=True)
    margin_applied = fields.Float('Applied margin', default=1.0)

    @api.model
    def get_taxes(self):
        setting = self.env['account.config.settings'].search([('company_id', '=', self.env.user.company_id.id)])
        if len(setting) > 0:
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
    @api.depends('men', 'men_quantity', 'installation', 'installation_qty', 'moving', 'moving_qty', 'moving_total', 'km', 'km_qty', 'sub_lines_total', 'margin_applied', 'miscellaneous_total')
    def _compute_totals(self):
        setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
        if len(setting) > 1:
            setting = setting[0]

        for line in self:
            # installation total
            if line.installation:
                if line.men:
                    line.installation_total = line.installation_qty * setting.installation_price * int(line.men_quantity)
                else:
                    line.installation_total = line.installation_qty * setting.installation_price
            else:
                line.installation_total = 0

            # moving total
            if line.moving:
                if line.men:
                    line.moving_total = line.moving_qty * setting.moving_price * int(line.men_quantity)
                else:
                    line.moving_total = line.moving_qty * setting.moving_price
            else:
                line.moving_total = 0

            # KM total
            if line.km:
                line.km_total = line.km_qty * setting.km_price
            else:
                line.km_total = 0

            # total without margin
            line.price_tmp = round(line.sub_lines_total + line.installation_total + line.moving_total + line.km_total + line.miscellaneous_total, 2)

            # total with margin
            line.price_unit = line.price_tmp * line.margin_applied

    # Inherited method
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        TODO: Why is the discount not taken into account
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_uom_qty, product=None, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

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
                        'list_price': line.price_unit,
                    })
                line.product_id = product_id.id
            else:
                line.product_id.name = line.name
                line.product_id.order_line_id = line.id
                line.product_id.list_price = line.price_unit
        return super(SaleOrderLine, self).write(values)      
