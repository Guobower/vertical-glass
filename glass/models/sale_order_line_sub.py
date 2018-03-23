# -*- coding: utf-8 -*-
"""
Sale order line extension
"""

import logging
from openerp import models, fields, api, _
from openerp.exceptions import Warning
_logger = logging.getLogger(__name__)


class SaleOrderLineSub(models.Model):
    _name = 'sale.order.line.sub'
    _description = 'Sub Order Line Shape'

    order_line_id = fields.Many2one('sale.order.line', 'Sale Order Line')

    type = fields.Selection([
        ('glass', 'Glass'),
        ('accessory', 'Accessory')],
        "Type", default='glass', required=True)

    description = fields.Text(string="Description", compute='_compute_description', store=True)

    edge_id = fields.Many2one('product.glass.edge', 'Edge')
    edge_width = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on W.', required=True, default=2)
    edge_height = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on H.', required=True, default=2)

    perimeter = fields.Float('Perimeter (M)', compute='_compute_perimeter', store=True)
    
    area_cost_price = fields.Float('Area Cost Price (m^2)', compute="_set_product_info")
    perimeter_cost_price = fields.Float('Perimeter Cost Price', compute="_set_product_info")

    area_total = fields.Float('Area Total', compute='_compute_sub_totals')
    perimeter_total = fields.Float('Perimeter Total', compute='_compute_sub_totals')

    multiplier = fields.Float('Multiplier', required=True, default=1.0)
    quantity = fields.Integer('Quantity', required=True, default=1)

    accessory_price = fields.Float('Acc. Price', default=0, compute="_set_product_info")
    total = fields.Float('Total', compute="_compute_total", required=True)

    use_glass_substitute = fields.Boolean('Use Glass Substitute', default=False)

    supplier_id = fields.Many2one('res.partner', 'Supplier')
    category_id = fields.Many2one('product.category', 'Category')
    glass_id = fields.Many2one('product.product', 'Glass')
    width = fields.Integer('Width (mm)', default=1000)
    height = fields.Integer('Height (mm)', default=1000)
    area_geometric = fields.Float('Area (m^2)', compute='_computeArea', store=True)
    area = fields.Float('Invoice Area (m^2)', compute='_computeArea', store=True)
    standard_price = fields.Float(related='glass_id.standard_price')
    lst_price = fields.Float(related='glass_id.lst_price')
    margin = fields.Float(related='category_id.margin_default')
    area_max_exceeded = fields.Boolean('Max area exceeded for the glass', default=False, readonly=True,
                                       compute="_computeArea")
    dimension_constraint_id = fields.Many2one('product.glass.dimconstraint', 'Dimension constraint')
    # TODO: There can be only one : are extras products with specific category or its own module
    extras_ids = fields.Many2many('product.glass.extra', string="Extras")
    accessory_id = fields.Many2one('product.product', 'Accessory')

    minimum_invoiceable = fields.Float('Minimum Invoiceable (m^2)', related='glass_id.minimum_invoiceable')
    braces_id = fields.Many2one('product.glass.braces', 'Braces')
    finish_id = fields.Many2one('product.glass.finish', 'Finish')
    shape_id = fields.Many2one('product.glass.shape', 'Shape')

    # Compute Area
    @api.one
    @api.depends('glass_id', 'width', 'height')
    def _computeArea(self):
        # Compute Area
        # in order to have the area in square meters (mm * mm => m^2)
        a = ((float(self.width) * float(self.height)) / 1000) / 1000
        if self.glass_id and self.glass_id.minimum_invoiceable and self.glass_id.minimum_invoiceable > a:
            a = self.glass_id.minimum_invoiceable

        # Set area
        self.area = a

        # Set price for area and shape
        if self.shape_id:
            self.area_cost_price = self.glass_id.lst_price * float(self.shape_id.multiplier)
        else:
            self.area_cost_price = self.glass_id.lst_price

        # Check if area is exceeded
        if 0 < self.glass_id.maximum_area_possible < self.area:
            self.area_max_exceeded = True
        else:
            self.area_max_exceeded = False
        self._compute_description()

    # Compute Perimeter
    @api.one
    @api.depends('width', 'height', 'edge_width', 'edge_height')
    def _compute_perimeter(self):
        # In order to have the area in meters
        p = ((float(self.width) * float(self.edge_width)) + (float(self.height) * float(self.edge_height))) / 1000
        self.perimeter = p
        if self.edge_id:
            self.perimeter_cost_price = float(self.edge_id.price)
        self._compute_description()

    # Set Product Related info
    @api.one
    @api.depends('glass_id', 'accessory_id', 'shape_id', 'edge_id')
    def _set_product_info(self):
        if self.type == 'glass':
            if self.shape_id:
                self.area_cost_price = self.glass_id.lst_price * float(self.shape_id.multiplier)
            else:
                self.area_cost_price = self.glass_id.lst_price
            if self.edge_id:
                self.perimeter_cost_price = float(self.edge_id.price)
        if self.type == 'accessory':
            self.accessory_price = self.accessory_id.lst_price
            self.total = self.quantity * self.accessory_price * self.multiplier
        self._compute_description()

    # Compute base prices
    @api.one
    @api.depends('perimeter')
    def _compute_base_price(self):
        # Perimeter total
        if self.edge_id:
            self.perimeter_cost_price = float(self.edge_id.price)
        else:
            self.perimeter_cost_price = 0
        self._compute_description()

    # Compute sub-totals
    @api.one
    @api.depends('area', 'area_cost_price', 'perimeter_cost_price', 'finish_id')
    def _compute_sub_totals(self):
        self.area_total = self.area * self.area_cost_price
        if self.finish_id and self.finish_id.price:
            self.area_total = self.area_total + (self.area * self.finish_id.price)
        self.perimeter_total = self.perimeter * self.perimeter_cost_price

    @api.one
    @api.depends('quantity', 'area_total', 'perimeter_total', 'multiplier')
    def _compute_total(self):
        if self.type == 'glass':
            self.total = self.quantity * (self.area_total + self.perimeter_total) * self.multiplier
        if self.type == 'accessory':
            self.total = self.quantity * self.accessory_price * self.multiplier
        self._compute_description()

    @api.one
    @api.depends('width', 'height', 'edge_width', 'edge_height', 'glass_id', 'accessory_id', 'shape_id', 'edge_id', 'area', 'area_cost_price', 'perimeter_cost_price', 'quantity', 'area_total', 'perimeter_total', 'multiplier', 'total', 'finish_id')
    def _compute_description(self):
        if self.type == 'glass':
            text = ''
            if self.glass_id:
                text = str(self.glass_id.categ_id.name.encode('utf-8')) + " - " + str(self.glass_id.name.encode('utf-8'))
            if self.quantity:
                text = text + "\n- " + str(self.quantity) + " volume(s) de " + str(self.width) + "mm x " + str(self.height) + "mm - "
                if self.shape_id:
                    text = text + str(self.shape_id.name.encode('utf-8'))
                if self.finish_id:
                    text = text + ", " + str(self.finish_id.name.encode('utf-8'))
            if self.area_max_exceeded:
                setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
                text = text + "\n /!\ " + str(setting.glass_maximum_area_warning.encode('utf-8'))
            if self.edge_id:
                text = text + "\n- " + str(self.edge_id.name.encode('utf-8')) + " (" + str(self.edge_width) + " / " + str(self.edge_height) + ")"
            self.description = text
        if self.type == 'accessory':
            self.description = str(self.accessory_id.categ_id.name.encode('utf-8')) + " - " + str(self.accessory_id.name.encode('utf-8'))

    @api.multi
    def change_glass_to_substitute(self):
        return {'value': {'use_glass_substitute': False, 'glass_id': self.glass_id.maximum_area_substitute, 'area_max_exceeded': False}}
