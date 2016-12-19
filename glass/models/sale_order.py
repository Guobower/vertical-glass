from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reference_auto = fields.Char('Reference auto', related='partner_id.ref_auto', store=True)
    header_text = fields.Html('Header text', default=lambda self: self._compute_header_text())
    header_text_replaced = fields.Html('Header text replaced', compute='_get_header_text')
    footer_text = fields.Html('Footer text', default=lambda self: self._compute_footer_text())
    footer_text_replaced = fields.Html('Footer text replaced', compute='_get_footer_text')

    @api.model
    def _compute_header_text(self):
        setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
        if len(setting) > 1:
            setting = setting[0]
        return setting.default_header_text

    @api.model
    def _compute_footer_text(self):
        setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
        if len(setting) > 1:
            setting = setting[0]
        return setting.default_footer_text

    @api.multi
    def print_technical(self):
        return self.env['report'].get_action(self, 'glass.sale_order_technical_report_template')

    @api.multi
    def print_full(self):
        return self.env['report'].get_action(self, 'glass.sale_order_ful_report_template')

    @api.one
    @api.depends('header_text')
    def _get_header_text(self):
        text = self.header_text
        text = text.replace('%(company)s', self.company_id.name)
        text = text.replace('%(internal_reference)s', self.name)
        text = text.replace('%(customer_reference)s', self.reference_auto)
        text = text.replace('%(customer_name)s', self.partner_id.name)
        text = text.replace('%(salesman)s', self.user_id.name)
        bank_account_ids = self.env['account.journal'].search([('company_id', '=', self.env.user.company_id.id), ('bank_acc_number', '!=', '')])
        if len(bank_account_ids) > 1:
            bank_account_ids = bank_account_ids[0]
        text = text.replace('%(bank_number)s', bank_account_ids.bank_acc_number)
        self.header_text_replaced = text
        return text.encode('utf-8')

    @api.one
    @api.depends('footer_text')
    def _get_footer_text(self):
        text = self.footer_text
        text = text.replace('%(company)s', self.company_id.name)
        text = text.replace('%(internal_reference)s', self.name)
        text = text.replace('%(customer_reference)s', self.reference_auto)
        text = text.replace('%(customer_name)s', self.partner_id.name)
        text = text.replace('%(salesman)s', self.user_id.name)
        bank_account_ids = self.env['account.journal'].search([('company_id', '=', self.env.user.company_id.id), ('bank_acc_number', '!=', '')])
        if len(bank_account_ids) >= 1:
            if len(bank_account_ids) > 1:
                bank_account_ids = bank_account_ids[0]
            text = text.replace('%(bank_number)s', bank_account_ids.bank_acc_number)
        self.footer_text_replaced = text
        return text.encode('utf-8')
