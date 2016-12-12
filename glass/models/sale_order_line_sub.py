from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLineSub(models.Model):
    _name = 'sale.order.line.sub'
    _description = 'Sub Order Line Shape'

    order_line_id = fields.Many2one('sale.order.line', 'Sale Order Line')
    type = fields.Selection([('glass', 'Glass'), ('accessory', 'Accessory')], "Type", default='glass', required=True)
    description = fields.Text(string="Description")

    glass_id = fields.Many2one('product.product', 'Glass')
    accessory_id = fields.Many2one('product.product', 'Accessory')

    shape_id = fields.Many2one('product.glass.shape', 'Shape')

    width = fields.Float('Width (mm)', default=100)
    height = fields.Float('Height (mm)', default=100)

    edge_id = fields.Many2one('product.glass.edge', 'Edge')
    edge_width = fields.Selection([(1,'1'),(2,'2')], 'Edges on W.', required=True, default=2)
    edge_height = fields.Selection([(1,'1'),(2,'2')], 'Edges on H.', required=True, default=2)

    area = fields.Float('Area (m^2)', compute='_computeArea', store=True)
    perimeter = fields.Float('Perimeter (M)', compute='_computePerimeter', store=True)
    
    area_cost_price = fields.Float('Area Cost Price', compute="_setProductInfo")
    perimeter_cost_price = fields.Float('Perimeter Cost Price', compute="_setProductInfo")

    area_total = fields.Float('Area Total', compute='_computeSubTotals')
    perimeter_total = fields.Float('Perimeter Total', compute='_computeSubTotals')

    supplier_id = fields.Many2one('res.partner', 'Supplier')
    
    multiplier = fields.Float('Multiplier', required=True, default=1.0)
    quantity_table = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15')]
    quantity = fields.Selection(quantity_table, 'Quantity', required=True, default=1)

    accessory_price = fields.Float('Acc. Price', default=0, compute="_setProductInfo")
    total = fields.Float('Total', compute="_computeTotal", required=True)

    # Compute Area
    @api.one
    @api.depends('width', 'height')
    def _computeArea(self):
        a = ((self.width * self.height) / 100) / 100 # to have the area in square meters (mm * mm => m^2)
        if self.glass_id and self.glass_id.minimum_invoicable and self.glass_id.minimum_invoicable > a:
            a = self.glass_id.minimum_invoicable
        self.area = a
        if self.shape_id:
            self.area_cost_price = self.glass_id.lst_price * float(self.shape_id.multiplier)
        else:
            self.area_cost_price = self.glass_id.lst_price

    # Compute Perimeter
    @api.one
    @api.depends('width', 'height', 'edge_width', 'edge_height')
    def _computePerimeter(self):
        p = ((self.width * self.edge_width) + (self.height * self.edge_height)) / 100 # to have the area in meters
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
