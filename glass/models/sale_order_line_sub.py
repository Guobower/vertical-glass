from openerp import models, fields, api
from openerp import _
from openerp.exceptions import Warning


import logging
_logger = logging.getLogger(__name__)

class SaleOrderLineSub(models.Model):
    _name = 'sale.order.line.sub'
    _description = 'Sub Order Line Shape'

    order_line_id = fields.Many2one('sale.order.line', 'Sale Order Line')
    currency_id = fields.Many2one('res.currency', related='order_line_id.currency_id', string='Currency')

    type = fields.Selection([('glass', 'Glass'), ('accessory', 'Accessory')], "Type", default='glass', required=True)

    category_id = fields.Many2one('product.category', 'Category')
    glass_id = fields.Many2one('product.product', 'Glass')
    accessory_id = fields.Many2one('product.product', 'Accessory')

    supplier_id = fields.Many2one('res.partner', 'Supplier')

    shape_id = fields.Many2one('product.glass.shape', 'Shape')

    width = fields.Integer('Width (mm)', default=1000)
    height = fields.Integer('Height (mm)', default=1000)

    edge_id = fields.Many2one('product.glass.edge', 'Edge')
    edge_width = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on W.', required=True, default=2)
    edge_height = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')], 'Edges on H.', required=True, default=2)

    finish_id = fields.Many2one('product.glass.finish', 'Finish')

    category_margin = fields.Float(related='category_id.margin', string="Margin (%)")
    price_unit_product = fields.Float(related='glass_id.price_with_auto_margin', string="Price (m^2)")

    area = fields.Float('Area (m^2)', compute='_computeArea', store=True)
    perimeter = fields.Float('Perimeter (m)', compute='_compute_perimeter', store=True)

    price_base = fields.Float(string="Base Price", compute='_compute_price_base')

    shape_margin = fields.Float(related='shape_id.margin', string="Margin (%)")
    price_shape = fields.Float(string="Shape Price", compute='_compute_price_shape')

    price_unit_finish = fields.Float(related='finish_id.price', string="Price (m^2)")
    price_finish = fields.Float(string="Finish Price", compute='_compute_price_finish')

    price_unit_edge = fields.Float(related='edge_id.price', string="Price (m)")
    price_edge = fields.Float(string="Edge Price", compute='_compute_price_edge')

    price_accessory = fields.Float(related='accessory_id.price_with_auto_margin', string="Price")

    margin = fields.Float('Margin (%)', required=True, default=0)
    quantity = fields.Integer('Quantity', required=True, default=1)

    subtotal_unit = fields.Float(string="Unit Sub-total", compute='_compute_subtotal_unit')
    subtotal = fields.Float(string="Sub-total", compute='_compute_subtotal')

    # accessory_price = fields.Float('Acc. Price', default=0, compute="_setProductInfo")
    total = fields.Float('Total', compute="_compute_total", required=True)

    area_max_exceeded = fields.Boolean('Max area exceeded for the glass', default=False)
    use_glass_substitude = fields.Boolean('Use Glass Substitude', default=False)

    description = fields.Text(string="Description", compute='_compute_description', store=True)

    # Compute Area
    @api.one
    @api.depends('width', 'height')
    def _computeArea(self):
        # Compute Area
        self.area = (float(self.width) * float(self.height)) / (1000 * 1000) # to have the area in square meters (mm * mm => m^2)
        if self.glass_id and self.glass_id.minimum_invoicable and self.glass_id.minimum_invoicable > self.area:
            self.area = self.glass_id.minimum_invoicable

        # Check if area is exceeded
        self.area_max_exceeded = self.glass_id.maximum_area_possible > 0 and self.glass_id.maximum_area_possible < self.area

        self._compute_description()

    @api.one
    @api.depends('glass_id', 'area')
    def _compute_price_base(self):
        self.price_base = self.area * self.price_unit_product

    @api.one
    @api.depends('price_base', 'shape_id')
    def _compute_price_shape(self):
        self.price_shape = self.price_base * self.shape_margin / 100

    @api.one
    @api.depends('finish_id', 'area')
    def _compute_price_finish(self):
        self.price_finish = self.price_unit_finish * self.area

    @api.one
    @api.depends('width', 'height', 'edge_width', 'edge_height')
    def _compute_perimeter(self):
        self.perimeter = ((float(self.width) * float(self.edge_width)) + (float(self.height) * float(self.edge_height))) / 1000 # to have the area in meters
        self._compute_description()

    @api.one
    @api.depends('edge_id', 'perimeter')
    def _compute_price_edge(self):
        self.price_edge = self.price_unit_edge * self.perimeter

    @api.one
    @api.depends('type', 'price_base', 'price_shape', 'price_finish', 'price_edge', 'accessory_id')
    def _compute_subtotal_unit(self):
        if self.type == 'glass':
            self.subtotal_unit = self.price_base + self.price_shape + self.price_finish + self.price_edge
        elif self.type == 'accessory':
            self.subtotal_unit = self.price_accessory

    @api.one
    @api.depends('subtotal_unit', 'quantity')
    def _compute_subtotal(self):
        self.subtotal = self.subtotal_unit * self.quantity

    # Set Product Related info
    @api.one
    @api.depends('subtotal', 'margin')
    def _compute_total(self):
        self.total = self.subtotal * (1 + self.margin / 100)
        #self._compute_description()

    @api.one
    @api.depends('total')
    def _compute_description(self):
        if self.type == 'glass':
            self.description = '\n'.join(filter(None, [
                str(self.glass_id.categ_id.name.encode('utf-8')) + " - " + str(self.glass_id.name.encode('utf-8')) if self.glass_id else '',
                '- ' + str(self.quantity) + " volume(s) de " + str(self.width) + "mm x " + str(self.height) + "mm" + (' - ' + str(self.shape_id.name.encode('utf-8')) if self.shape_id else ''),
                '/!\ ' + str(self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)]).glass_maximum_area_warning.encode('utf-8')) if self.area_max_exceeded else '',
                '- ' + str(self.finish_id.name.encode('utf-8')) if self.finish_id else '',
                "- " + str(self.edge_id.name.encode('utf-8')) + " (" + str(self.edge_width) + " / " + str(self.edge_height) + ")" if self.edge_id else '',
            ]))
        elif self.type == 'accessory':
            self.description = str(self.accessory_id.categ_id.name.encode('utf-8')) + " - " + str(self.accessory_id.name.encode('utf-8'))

        _logger.info('\n\n'+str(self.description)+'\n\n')

    @api.multi
    def change_glass_to_substitude(self):
        return {
            'value': {
                'use_glass_substitude': False,
                'glass_id': self.glass_id.maximum_area_substitute,
                'area_max_exceeded': False
            }
        }
