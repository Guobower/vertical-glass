from openerp import models, fields, api

class SaleOrderLineSub(models.Model):
    _name = 'sale.order.line.sub'
    _description = 'Sub Order Line Shape'

    order_line_id = fields.Many2one('sale.order.line', 'Sale Order Line', required=True)

    glass_id = fields.Many2one('product.product', 'Product', required=True)
    shape_id = fields.Many2one('product.glass.shape', 'Shape')

    width = fields.Float('Width (mm)', default=100)
    height = fields.Float('Height (mm)', default=100)

    edge_id = fields.Many2one('product.glass.edge', 'Edge')
    edge_width = fields.Selection([(1,'1'),(2,'2')], 'Edges on width')
    edge_height = fields.Selection([(1,'1'),(2,'2')], 'Edges on height')

    area = fields.Float('Area', compute='_computeArea', store=True)
    area_cost_price = fields.Float('Area Cost Price')

    perimeter = fields.Float('Perimeter', compute='_computePerimeter', store=True)
    perimeter_cost_price = fields.Float('Perimeter Cost Price')
    supplier_id = fields.Many2one('res.partner', 'Supplier')
    
    multiplier = fields.Float('Multiplier', required=True, default=1)
    qantity = fields.Integer('Quantity', required=True, default=1)
    
    total = fields.Float('Total', required=True)

    @api.depends('glass_id', 'width', 'height')
    def _computeArea(self):
        for line in self:
            a = (line.width * line.height) / 100 # to have the area in quare meters
            if line.glass_id.minimum_invoicable and line.glass_id.minimum_invoicable > a:
                a = line.glass_id.minimum_invoicable
            line.area = a

    @api.depends('glass_id', 'width', 'height')
    def _computePerimeter(self):
        for line in self:
            a = ((line.width + line.height) * 2) / 100 # to have the area in

