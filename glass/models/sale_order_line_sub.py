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
    description = fields.Text(string="Description", compute='_compute_description', store=True)

    type = fields.Selection([('glass', 'Glass'), ('accessory', 'Accessory')], string="Sub Type", default='glass', required=True)
    category_id = fields.Many2one('product.category', 'Category')

    glass_front_id = fields.Many2one('product.product', 'Glass (front)')
    glass_back_id = fields.Many2one('product.product', 'Glass (back)')
    glass_middle_id = fields.Many2one('product.product', 'Glass (middle)')

    shape_id = fields.Many2one('product.glass.shape', 'Shape')
    width = fields.Integer('Width (mm)', default=1000)
    height = fields.Integer('Height (mm)', default=1000)

    edge_id = fields.Many2one('product.glass.edge', 'Edge')
    edge_width = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on W.', required=True, default=2)
    edge_height = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on H.', required=True, default=2)

    perimeter = fields.Float('Perimeter (M)', compute='compute_perimeter', store=True)
    perimeter_cost_price = fields.Float('Perimeter Cost Price', compute="compute_perimeter")
    perimeter_total = fields.Float('Perimeter Total', compute='compute_perimeter')

    area = fields.Float('Invoice Area (m^2)', compute='compute_area', store=True)
    area_geometric = fields.Float('Area (m^2)', compute='compute_area', store=True)
    area_total = fields.Float('Area Total', compute='compute_area')
    area_cost_price = fields.Float('Area Cost Price (m^2)', compute="compute_area")

    minimum_invoiceable = fields.Float('Minimum Invoiceable (m^2)', related='glass_front_id.minimum_invoiceable')

    area_max_exceeded_front = fields.Boolean('Max area exceeded for the front glass', default=False, readonly=True, compute="compute_area")
    area_max_exceeded_back = fields.Boolean('Max area exceeded for the back glass', default=False, readonly=True, compute="compute_area")
    area_max_exceeded_middle = fields.Boolean('Max area exceeded for the middle glass', default=False, readonly=True, compute="compute_area")

    use_glass_substitute = fields.Boolean('Use Glass Substitute', default=False)
    # Options
    braces_id = fields.Many2one('product.glass.braces', 'Braces')
    divider_id = fields.Many2one('product.glass.divider', 'Divider')
    finish_id = fields.Many2one('product.glass.finish', 'Finish')
    options_total = fields.Float('Total options', compute="compute_options", readonly=True, default=0)
    # Extras
    extras_ids = fields.Many2many('product.glass.extra', string="Extras")
    extras_total = fields.Float('Total extras', compute="compute_extras", readonly=True, default=0)
    # Accessory
    accessory_id = fields.Many2one('product.product', 'Accessory')
    accessory_price = fields.Float('Acc. Price', default=0, compute="compute_accessory")

    multiplier = fields.Float('Multiplier', required=True, default=1.0)
    quantity = fields.Integer('Quantity', required=True, default=1)
    total = fields.Float('Total', compute="_compute_total", required=True)

    # TBD
    supplier_id = fields.Many2one('res.partner', 'Supplier')
    standard_price = fields.Float(related='glass_front_id.standard_price')
    lst_price = fields.Float(related='glass_front_id.lst_price')
    margin = fields.Float(related='category_id.margin_default')
    dimension_constraint_id = fields.Many2one('product.glass.dimconstraint', 'Dimension constraint')

    @api.onchange('glass_front_id')
    def get_glass_product_presets(self):
        """
        load preset taken from main glass product
        """
        if self.glass_front_id.glass_back_id:
            self.glass_back_id = self.glass_front_id.glass_back_id
        if self.glass_front_id.glass_middle_id:
            self.glass_middle_id = self.glass_front_id.glass_middle_id
        if self.glass_front_id.product_extras_ids:
            self.extras_ids = self.glass_front_id.product_extras_ids

    @api.one
    @api.depends('glass_front_id', 'width', 'height')
    def compute_area(self):
        """ Compute Area
        both geometric and invoiceable area
        """
        self.area = 0
        self.area_total = 0
        self.area_geometric = 0
        self.area_cost_price = 0
        unit_area = ((float(self.width) * float(self.height)) / 1000) / 1000

        if self.glass_front_id:
            # in order to have the area in square meters (mm * mm => m^2)
            a = unit_area
            if self.glass_front_id.minimum_invoiceable and self.glass_front_id.minimum_invoiceable > unit_area:
                a = self.glass_front_id.minimum_invoiceable
                self.area += self.glass_front_id.minimum_invoiceable
            else:
                self.area += unit_area
            # Set area - actually area of 1 item
            self.area_geometric += unit_area
            self.area_cost_price = self.glass_front_id.list_price

            # Check if area is exceeded
            if 0 < self.glass_front_id.maximum_area_possible < a:
                self.area_max_exceeded_front = True
            else:
                self.area_max_exceeded_front = False

        if self.glass_back_id:
            # in order to have the area in square meters (mm * mm => m^2)
            a = unit_area
            if self.glass_back_id.minimum_invoiceable and self.glass_back_id.minimum_invoiceable > unit_area:
                a = self.glass_back_id.minimum_invoiceable
                self.area += self.glass_back_id.minimum_invoiceable
            else:
                self.area += unit_area
            # Set area - actually area of 1 item
            self.area_geometric += unit_area
            self.area_cost_price += self.glass_back_id.list_price

            # Check if area is exceeded
            if 0 < self.glass_back_id.maximum_area_possible < a:
                self.area_max_exceeded_back = True
            else:
                self.area_max_exceeded_back = False

        if self.glass_middle_id:
            # in order to have the area in square meters (mm * mm => m^2)
            a = unit_area
            if self.glass_middle_id.minimum_invoiceable and self.glass_middle_id.minimum_invoiceable > unit_area:
                a = self.glass_middle_id.minimum_invoiceable
                self.area += self.glass_middle_id.minimum_invoiceable
            else:
                self.area += unit_area
            # Set area - actually area of 1 item
            self.area_geometric += unit_area
            self.area_cost_price += self.glass_middle_id.list_price

            # Check if area is exceeded
            if 0 < self.glass_middle_id.maximum_area_possible < a:
                self.area_max_exceeded_middle = True
            else:
                self.area_max_exceeded_middle = False

        # Set price for area and shape
        if self.shape_id:
            self.area_cost_price = self.area_cost_price*float(self.shape_id.multiplier)

        self.area_total = self.area * self.area_cost_price

        self._compute_description()

    @api.one
    @api.depends('width', 'height', 'edge_width', 'edge_height')
    def compute_perimeter(self):
        """ In order to have the area perimeter in meters we divide by 1000
        """
        self.perimeter = ((float(self.width) * float(self.edge_width)) +
                          (float(self.height) * float(self.edge_height))) / 1000
        if self.edge_id:
            self.perimeter_cost_price = float(self.edge_id.price)
        self.perimeter_total = self.perimeter * self.perimeter_cost_price

        self._compute_description()

    @api.one
    @api.depends('accessory_id')
    def compute_accessory(self):
        self.accessory_price = self.accessory_id.lst_price
        self._compute_description()

    @api.one
    @api.onchange('finish_id', 'divider_id', 'braces_id')
    def compute_options(self):
        self.options_total = 0
        if self.finish_id and self.finish_id.price:
            self.options_total += self.finish_id.compute_price(self.area_geometric)
        if self.divider_id and self.divider_id.price:
            self.options_total += self.divider_id.compute_price(self.area_geometric)
        if self.braces_id and self.braces_id.price:
            self.options_total += self.braces_id.compute_price()
        self._compute_description()

    @api.one
    @api.depends('extras_ids')
    def compute_extras(self):
        self.extras_total = 0
        if self.extras_ids:
            for line in self.extras_ids:
                self.extras_total += line.price
            self.extras_total = self.extras_total * self.area_geometric
        self._compute_description()

    @api.one
    @api.depends('quantity', 'area_total', 'perimeter_total', 'multiplier')
    def _compute_total(self):
        if self.type == 'glass':
            self.total = self.options_total + self.extras_total + self.area_total + self.perimeter_total
            # apply quantity and correction rate
            self.total = self.quantity * self.area_total * self.multiplier
        if self.type == 'accessory':
            self.total = self.quantity * self.accessory_price * self.multiplier
        self._compute_description()

    @api.one
    def _compute_description(self):
        if self.type == 'glass':
            text = ''
            if self.glass_front_id:
                text += "Front: {} - {}".format(self.glass_front_id.categ_id.name.encode('utf-8'), self.glass_front_id.name.encode('utf-8'))
            if self.glass_back_id:
                text += "\nBack: {} - {}".format(self.glass_back_id.categ_id.name.encode('utf-8'), self.glass_back_id.name.encode('utf-8'))
            if self.glass_middle_id:
                text += "\nMiddle: {} - {}".format(self.glass_middle_id.categ_id.name.encode('utf-8'),self.glass_middle_id.name.encode('utf-8'))
            if self.quantity:
                text += "\n- {} volume(s) de {} mm x {} mm".format(self.quantity, self.width, self.height)
                if self.shape_id:
                    text += ", " + str(self.shape_id.name.encode('utf-8'))
                if self.finish_id:
                    text += ", " + str(self.finish_id.name.encode('utf-8'))
                if self.divider_id:
                    text += ", " + str(self.divider_id.name.encode('utf-8'))
                if self.braces_id:
                    text += ", " + str(self.braces_id.name.encode('utf-8'))
            if self.area_max_exceeded_front or self.area_max_exceeded_back or self.area_max_exceeded_middle:
                setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
                text += "\n /!\ "
                if self.area_max_exceeded_front:
                    text += "\n /!\ [{}]".format(self.glass_front_id.name.encode('utf-8'))
                if self.area_max_exceeded_back:
                    text += "\n /!\ [{}]".format(self.glass_back_id.name.encode('utf-8'))
                if self.area_max_exceeded_middle:
                    text += "\n /!\ [{}]".format(self.glass_middle_id.name.encode('utf-8'))
                text += "\n /!\ " + str(setting.glass_maximum_area_warning.encode('utf-8'))
            if self.edge_id:
                text += "\n- " + str(self.edge_id.name.encode('utf-8')) + " (" + str(self.edge_width) + " / " + str(self.edge_height) + ")"
            self.description = text
        if self.type == 'accessory':
            self.description = str(self.accessory_id.categ_id.name.encode('utf-8')) + " - " + str(self.accessory_id.name.encode('utf-8'))

    @api.multi
    @api.onchange('use_glass_substitute')
    def change_glass_to_substitute(self):
        """
        This will replace any glass product that has exceeded the max area constraint for a registered substitute
        product. When replacement product doesn't exist no action will take place and the warning will still be on.
        """
        ret = {'value': {
            'use_glass_substitute': False
        }}
        if self.area_max_exceeded_front and self.glass_front_id and self.glass_front_id.maximum_area_substitute:
            ret['value'].update({
                'glass_front_id': self.glass_front_id.maximum_area_substitute,
                'are_max_exceeded_front': False
            })
        if self.area_max_exceeded_back and self.glass_back_id and self.glass_back_id.maximum_area_substitute:
            ret['value'].update({
                'glass_back_id': self.glass_back_id.maximum_area_substitute,
                'are_max_exceeded_back': False
            })
        if self.area_max_exceeded_back and self.glass_middle_id and self.glass_middle_id.maximum_area_substitute:
            ret['value'].update({
                'glass_middle_id': self.glass_middle_id.maximum_area_substitute,
                'are_max_exceeded_middle': False
            })

        return ret
