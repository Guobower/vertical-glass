# -*- coding: utf-8 -*-
"""
Sale order line extension
"""

import logging
from openerp import models, fields, api
_logger = logging.getLogger(__name__)


class SaleOrderLineSub(models.Model):
    """
    Main class
    """
    _name = 'sale.order.line.sub'
    _description = 'Sub Order Line Shape'

    order_line_id = fields.Many2one('sale.order.line', 'Sale Order Line')
    currency_id = fields.Many2one(related='order_line_id.currency_id')
    description = fields.Text(compute='_compute_description', default='', store=True)

    type = fields.Selection([('glass', 'Glass'), ('accessory', 'Accessory')], string="Sub Type",
                            default='glass', required=True)
    category_id = fields.Many2one('product.category', 'Category')

    glass_front_id = fields.Many2one('product.product', 'Glass (front)')
    glass_back_id = fields.Many2one('product.product', 'Glass (back)')
    glass_middle_id = fields.Many2one('product.product', 'Glass (middle)')
    # NOTE: we make the assumption that all glass products in this SubSOL are provided by the same supplier
    supplier_id = fields.Many2one('res.partner')

    shape_id = fields.Many2one('product.glass.shape', 'Shape')
    width = fields.Integer('Width (mm)', default=1000)
    height = fields.Integer('Height (mm)', default=1000)

    edge_id = fields.Many2one('product.glass.edge', 'Edge')
    edge_width = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on W.', required=True, default=2)
    edge_height = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on H.', required=True, default=2)

    perimeter = fields.Float('Perimeter (m)', compute='_compute_perimeter', store=True)
    perimeter_cost_price = fields.Float(string='Perimeter Cost price (m)', compute="_compute_perimeter")
    perimeter_total = fields.Float(compute='_compute_perimeter')

    area = fields.Float('Invoice Area (m^2)', compute='_compute_area', store=True)
    area_geometric = fields.Float('Area (m^2)', compute='_compute_area', store=True)
    area_total = fields.Float(compute='_compute_area')
    area_cost_price = fields.Float('Area Cost Price (m^2)', compute="_compute_area")

    minimum_invoiceable = fields.Float('Minimum Invoiceable (m^2)', related='glass_front_id.minimum_invoiceable')

    area_max_exceeded_front = fields.Boolean('Max area exceeded for the front glass', default=False,
                                             readonly=True, compute="_compute_area")
    area_max_exceeded_back = fields.Boolean('Max area exceeded for the back glass', default=False,
                                            readonly=True, compute="_compute_area")
    area_max_exceeded_middle = fields.Boolean('Max area exceeded for the middle glass', default=False,
                                              readonly=True, compute="_compute_area")

    use_glass_substitute = fields.Boolean(default=False)
    # Options
    grid_id = fields.Many2one('product.glass.grid')
    grid_colour = fields.Char()
    grid_socket_qty = fields.Integer(default=1)
    spacer_id = fields.Many2one('product.glass.spacer')
    finish_id = fields.Many2one('product.glass.finish')
    options_total = fields.Float('Total options', compute="_compute_options", readonly=True, default=0)
    dimconstraint_id = fields.Many2one('product.glass.dimconstraint')
    # Extras
    extras_ids = fields.Many2many('product.glass.extra', string="Extras")
    extras_total = fields.Float('Total extras', compute="_compute_extras", readonly=True, default=0)
    # Accessory
    accessory_id = fields.Many2one('product.product', 'Accessory')
    accessory_price = fields.Float('Acc. Price', default=0, compute="_compute_accessory")

    multiplier = fields.Float(required=True, default=1.0)
    quantity = fields.Integer(required=True, default=1)
    total = fields.Float(compute="_compute_total", required=True)

    @api.model
    def create(self, values):
        """ Make sur description is saved to db"""
        # update description
        if not values.get('description'):
            self._compute_description()
            values['description'] = self.description
        return super(SaleOrderLineSub, self).create(values)

    @api.multi
    def write(self, values):
        """Make sure description is saved to db"""
        if not values.get('description'):
            self._compute_description()
            values['description'] = self.description
        return super(SaleOrderLineSub, self).write(values)

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
    @api.depends('glass_front_id', 'width', 'height', 'shape_id')
    def _compute_area(self):
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
            area = unit_area
            if self.glass_front_id.minimum_invoiceable and self.glass_front_id.minimum_invoiceable > unit_area:
                area = self.glass_front_id.minimum_invoiceable
                self.area += self.glass_front_id.minimum_invoiceable
            else:
                self.area += unit_area
            # Set area - actually area of 1 item
            self.area_geometric += unit_area
            self.area_cost_price = self.glass_front_id.list_price

            # Check if area is exceeded
            self.area_max_exceeded_front = bool(0 < self.glass_front_id.maximum_area_possible < area)

        if self.glass_back_id:
            # in order to have the area in square meters (mm * mm => m^2)
            area = unit_area
            if self.glass_back_id.minimum_invoiceable and self.glass_back_id.minimum_invoiceable > unit_area:
                area = self.glass_back_id.minimum_invoiceable
                self.area += self.glass_back_id.minimum_invoiceable
            else:
                self.area += unit_area
            # Set area - actually area of 1 item
            self.area_geometric += unit_area
            self.area_cost_price += self.glass_back_id.list_price

            # Check if area is exceeded
            self.area_max_exceeded_back = bool(0 < self.glass_back_id.maximum_area_possible < area)

        if self.glass_middle_id:
            # in order to have the area in square meters (mm * mm => m^2)
            area = unit_area
            if self.glass_middle_id.minimum_invoiceable and self.glass_middle_id.minimum_invoiceable > unit_area:
                area = self.glass_middle_id.minimum_invoiceable
                self.area += self.glass_middle_id.minimum_invoiceable
            else:
                self.area += unit_area
            # Set area - actually area of 1 item
            self.area_geometric += unit_area
            self.area_cost_price += self.glass_middle_id.list_price

            # Check if area is exceeded
            self.area_max_exceeded_middle = bool(0 < self.glass_middle_id.maximum_area_possible < area)

        # Set price for area and shape
        if self.shape_id:
            self.area_cost_price = self.area_cost_price*float(self.shape_id.multiplier)

        # Check dimension constraints
        dim_constraint_rate = 1.0
        self.dimconstraint_id = None
        rules = self.env['product.glass.dimconstraint'].search([], order='rate desc')
        for rule in rules:
            # Area max
            if rule.mode == 'area':
                if self.area > rule.area:
                    self.dimconstraint_id = rule
                    dim_constraint_rate += float(rule.rate)/100
                    break
            # Inside rectangle
            elif rule.mode == 'inside_rectangle':
                if not self.can_be_inserted_inside_shape(rule):
                    self.dimconstraint_id = rule
                    dim_constraint_rate += float(rule.rate)/100
                    break
            else:
                self.dimconstraint_id = None

        # Apply the constraint if exists
        self.area_cost_price = self.area_cost_price * dim_constraint_rate
        self.area_total = self.area * self.area_cost_price

        self._compute_description()

    # This method tests if the current shape with dimension can be inserted inside the rule dimensions
    @api.model
    def can_be_inserted_inside_shape(self, rule):
        # We always use an "horizontal rectangle" : where the width is greater or equal than the height
        # Variables
        order_dim = {
            'width': self.width if self.width >= self.height else self.height,
            'height': self.height if self.height <= self.width else self.width,
        }
        rule_dim = {
            'width': rule.width if rule.width >= rule.height else rule.height,
            'height': rule.height if rule.height <= rule.width else rule.width,
        }
        _logger.debug("Order: %s | Rule: %s", order_dim, rule_dim)

        # Test
        if (order_dim['width'] > rule_dim['width'] or order_dim['height'] > rule_dim['height']):
            return False
        return True

    @api.one
    @api.depends('width', 'height', 'edge_width', 'edge_height', 'edge_id')
    def _compute_perimeter(self):
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
    def _compute_accessory(self):
        self.accessory_price = self.accessory_id.lst_price
        self._compute_description()

    @api.one
    @api.onchange('finish_id', 'spacer_id', 'grid_id', 'grid_socket_qty')
    def _compute_options(self):
        self.options_total = 0
        if self.finish_id and self.finish_id.price:
            self.options_total += self.finish_id.compute_price(self.area_geometric)
        if self.spacer_id and self.spacer_id.price:
            self.options_total += self.spacer_id.compute_price(self.area_geometric)
        if self.grid_socket_qty > 1 and self.grid_id:
            self.options_total += self.grid_id.price * self.grid_socket_qty
        elif self.grid_socket_qty == 1:
            self.grid_id = None
            self.grid_colour = ''
            
        self._compute_description()

    @api.one
    @api.depends('extras_ids')
    def _compute_extras(self):
        self.extras_total = 0
        if self.extras_ids:
            for line in self.extras_ids:
                self.extras_total += line.price
            self.extras_total = self.extras_total * self.area_geometric
        self._compute_description()

    @api.one
    @api.depends('quantity', 'area_total', 'perimeter_total', 'multiplier')
    @api.onchange('accessory_id')
    def _compute_total(self):
        if self.type == 'glass':
            self.total = self.options_total + self.extras_total + self.area_total + self.perimeter_total
            # apply quantity and correction rate
            self.total = self.quantity * self.total * self.multiplier
        if self.type == 'accessory':
            self.total = self.quantity * self.accessory_price * self.multiplier
        self._compute_description()

    @api.one
    @api.depends('type', 'total')
    def _compute_description(self):
        text = ''
        if self.type == 'glass':
            if self.glass_front_id:
                text += "Front: {} - {}".format(self.glass_front_id.categ_id.name.encode('utf-8'),
                                                self.glass_front_id.name.encode('utf-8'))
            if self.glass_back_id:
                text += "\nBack: {} - {}".format(self.glass_back_id.categ_id.name.encode('utf-8'),
                                                 self.glass_back_id.name.encode('utf-8'))
            if self.glass_middle_id:
                text += "\nMiddle: {} - {}".format(self.glass_middle_id.categ_id.name.encode('utf-8'),
                                                   self.glass_middle_id.name.encode('utf-8'))
            if self.quantity:
                text += "\n- {} volume(s) de {} mm x {} mm".format(self.quantity, self.width, self.height)
                if self.shape_id:
                    text += ", " + str(self.shape_id.name.encode('utf-8'))
                if self.finish_id:
                    text += ", " + str(self.finish_id.name.encode('utf-8'))
                if self.spacer_id:
                    text += ", " + str(self.spacer_id.name.encode('utf-8'))
                if self.grid_socket_qty > 1:
                    text += ", " + str(self.grid_socket_qty) + " alvéoles"
                    if self.grid_id:
                        text += " " + str(self.grid_id.name.encode('utf-8'))
                        if self.grid_colour:
                            text += " (couleur : " + str(self.grid_colour) + ")"
            if self.area_max_exceeded_front or self.area_max_exceeded_back or self.area_max_exceeded_middle:
                setting = self.env['glass.sale.config.settings.data'].search([
                    ('company_id', '=', self.env.user.company_id.id)])
                text += r"\n /!\ "
                if self.area_max_exceeded_front:
                    text += r"\n /!\ [{}]".format(self.glass_front_id.name.encode('utf-8'))
                if self.area_max_exceeded_back:
                    text += r"\n /!\ [{}]".format(self.glass_back_id.name.encode('utf-8'))
                if self.area_max_exceeded_middle:
                    text += r"\n /!\ [{}]".format(self.glass_middle_id.name.encode('utf-8'))
                text += r"\n /!\ " + str(setting.glass_maximum_area_warning.encode('utf-8'))
            if self.edge_id:
                text += "\n- {} ({} / {})".format(str(self.edge_id.name.encode('utf-8')),
                                                  str(self.edge_width),
                                                  str(self.edge_height))
        elif self.type == 'accessory':
            if self.accessory_id:
                text = "{}".format(self.accessory_id.name.encode('utf-8'))
                if self.accessory_id.categ_id:
                    text = "{} - {}".format(self.accessory_id.categ_id.name.encode('utf-8'), text)
        self.description = text

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
