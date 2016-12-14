from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reference_auto = fields.Char('Reference auto', related='partner_id.ref_auto', store=True)
    header_text = fields.Html('Header text', default=lambda self: self._compute_header_text())
    footer_text = fields.Html('Footer text', default=lambda self: self._compute_footer_text())

    @api.model
    def _compute_header_text(self):
        setting = self.env['glass.sale.config.settings.data'].search([])
        if len(setting) > 1:
            setting = setting[0]
        return setting.default_header_text

    @api.model
    def _compute_footer_text(self):
        setting = self.env['glass.sale.config.settings.data'].search([])
        if len(setting) > 1:
            setting = setting[0]
        return setting.default_footer_text

    @api.multi
    def print_technical(self):
        return self.env['report'].get_action(self, 'glass.sale_order_technical_report_template')

    @api.multi
    def print_full(self):
        return self.env['report'].get_action(self, 'glass.sale_order_ful_report_template')