from openerp import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reference_auto = fields.Char('Reference auto', related='partner_id.ref_auto', store=True)
    header_text = fields.Html('Header text')
    footer_text = fields.Html('Footer text')