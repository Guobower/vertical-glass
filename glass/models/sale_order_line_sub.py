from openerp import models, fields, api
from openerp import _
from openerp.exceptions import Warning


import logging
_logger = logging.getLogger(__name__)

class SaleOrderLineSub(models.Model):
    _name = 'sale.order.line.sub'
    _description = 'Sub Order Line Shape'

    order_line_id = fields.Many2one('sale.order.line', 'Sale Order Line')
    type = fields.Selection([('glass', 'Glass'), ('accessory', 'Accessory')], "Type", default='glass', required=True)
    description = fields.Text(string="Description", compute='_compute_description', store=True)

    glass_id = fields.Many2one('product.product', 'Glass')
    accessory_id = fields.Many2one('product.product', 'Accessory')

    shape_id = fields.Many2one('product.glass.shape', 'Shape')

    width = fields.Integer('Width (mm)', default=1000)
    height = fields.Integer('Height (mm)', default=1000)

    edge_id = fields.Many2one('product.glass.edge', 'Edge')
    edge_width = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on W.', required=True, default=2)
    edge_height = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on H.', required=True, default=2)

    area = fields.Float('Area (m^2)', compute='_computeArea', store=True)
    perimeter = fields.Float('Perimeter (M)', compute='_computePerimeter', store=True)
    
    area_cost_price = fields.Float('Area Cost Price', compute="_setProductInfo")
    perimeter_cost_price = fields.Float('Perimeter Cost Price', compute="_setProductInfo")

    area_total = fields.Float('Area Total', compute='_computeSubTotals')
    perimeter_total = fields.Float('Perimeter Total', compute='_computeSubTotals')

    supplier_id = fields.Many2one('res.partner', 'Supplier')

    multiplier = fields.Float('Multiplier', required=True, default=1.0)
    quantity = fields.Integer('Quantity', required=True, default=1)

    accessory_price = fields.Float('Acc. Price', default=0, compute="_setProductInfo")
    total = fields.Float('Total', compute="_computeTotal", required=True)

    area_max_exceeded = fields.Boolean('Max area exceeded for the glass', default=False)
    use_glass_substitude = fields.Boolean('Use Glass Substitude', default=False)

    # Compute Area
    @api.one
    @api.depends('glass_id', 'width', 'height')
    def _computeArea(self):
        # Compute Area
        a = ((float(self.width) * float(self.height)) / 1000) / 1000 # to have the area in square meters (mm * mm => m^2)
        if self.glass_id and self.glass_id.minimum_invoicable and self.glass_id.minimum_invoicable > a:
            a = self.glass_id.minimum_invoicable

        # Set area
        self.area = a

        # Set price for area and shape
        if self.shape_id:
            self.area_cost_price = self.glass_id.lst_price * float(self.shape_id.multiplier)
        else:
            self.area_cost_price = self.glass_id.lst_price

        # Check if area is exceeded
        if self.glass_id.maximum_area_possible > 0 and self.glass_id.maximum_area_possible < self.area:
            self.area_max_exceeded = True
        else:
            self.area_max_exceeded = False

    # Compute Perimeter
    @api.one
    @api.depends('width', 'height', 'edge_width', 'edge_height')
    def _computePerimeter(self):
        p = ((float(self.width) * float(self.edge_width)) + (float(self.height) * float(self.edge_height))) / 1000 # to have the area in meters
        self.perimeter = p
        if self.edge_id:
            self.perimeter_cost_price = float(self.edge_id.price)

    # Set Product Related info
    @api.one
    @api.depends('glass_id', 'accessory_id', 'shape_id', 'edge_id')
    def _setProductInfo(self):
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

    # Compute base prices
    @api.one
    @api.depends('perimeter')
    def _computeBasePrice(self):
        # Perimeter total
        if self.edge_id:
            self.perimeter_cost_price = float(self.edge_id.price)
        else:
            self.perimeter_cost_price = 0

    # Compute sub-totals
    @api.one
    @api.depends('area', 'area_cost_price', 'perimeter_cost_price')
    def _computeSubTotals(self):
        self.area_total = self.area * self.area_cost_price
        self.perimeter_total = self.perimeter * self.perimeter_cost_price

    @api.one
    @api.depends('quantity', 'area_total', 'perimeter_total', 'multiplier')
    def _computeTotal(self):
        if self.type == 'glass':
            self.total = self.quantity * (self.area_total + self.perimeter_total) * self.multiplier
        if self.type == 'accessory':
            self.total = self.quantity * self.accessory_price * self.multiplier

    @api.one
    @api.depends('total')
    def _compute_description(self):
        if self.type == 'glass':
            text = ''
            if self.glass_id:
                text = str(self.glass_id.categ_id.name.encode('utf-8')) + " - " + str(self.glass_id.name.encode('utf-8'))
            if self.quantity:
                text = text + "\n- " + str(self.quantity) + " volume(s) de " + str(self.width) + "mm x " + str(self.height) + "mm"
            if self.area_max_exceeded:
                setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
                text = text + "\n /!\ " + str(setting.glass_maximum_area_warning.encode('utf-8'))
            if self.edge_id:
                text = text + "\n- " + str(self.edge_id.name.encode('utf-8')) + " (" + str(self.edge_width) + " / " + str(self.edge_height) + ")"
            self.description = text
        if self.type == 'accessory':
            self.description = str(self.accessory_id.categ_id.name.encode('utf-8')) + " - " + str(self.accessory_id.name.encode('utf-8'))

    @api.multi
    def change_glass_to_substitude(self):
        return {'value': {'use_glass_substitude': False, 'glass_id': self.glass_id.maximum_area_substitute, 'area_max_exceeded': False}}
