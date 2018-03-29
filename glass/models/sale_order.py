# -*- coding: utf-8 -*-
"""
Extends the sale.order model to include glass centric fields & methods
"""
import logging
from openerp import models, fields, api
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    """ Main class """
    _inherit = 'sale.order'

    reference_auto = fields.Char(related='partner_id.ref_auto', store=True)
    header_text = fields.Html(default=lambda self: self.do_set_header())
    header_text_replaced = fields.Html(compute='_compute_header_text')
    footer_text = fields.Html(default=lambda self: self.do_set_footer())
    footer_text_replaced = fields.Html(compute='_compute_footer_text')

    @api.model
    def do_set_header(self):
        """ Load header text using settings """
        setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
        if len(setting) > 1:
            setting = setting[0]
        return setting.default_header_text

    @api.model
    def do_set_footer(self):
        """ Load footer text using settings """
        setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
        if len(setting) > 1:
            setting = setting[0]
        return setting.default_footer_text

    @api.multi
    def print_technical(self):
        """ Generate technical report"""
        return self.env['report'].get_action(self, 'glass.sale_order_technical_report_template')

    @api.multi
    def print_full(self):
        """ Generate full quotation report """
        return self.env['report'].get_action(self, 'glass.sale_order_ful_report_template')

    @api.one
    @api.depends('header_text')
    def _compute_header_text(self):
        """ Replace patterns in header before saving """
        text = self.header_text
        text = text.replace('%(company)s', self.company_id.name)
        text = text.replace('%(internal_reference)s', self.name)
        text = text.replace('%(customer_reference)s', self.reference_auto)
        text = text.replace('%(customer_name)s', self.partner_id.name)
        text = text.replace('%(salesman)s', self.user_id.name)
        bank_account_ids = self.env['account.journal'].search([
            ('company_id', '=', self.env.user.company_id.id),
            ('bank_acc_number', '!=', '')])
        if len(bank_account_ids) > 0:
            if len(bank_account_ids) > 1:
                bank_account_ids = bank_account_ids[0]
            text = text.replace('%(bank_number)s', bank_account_ids.bank_acc_number)
        self.header_text_replaced = text
        return text.encode('utf-8')

    @api.one
    @api.depends('footer_text')
    def _compute_footer_text(self):
        """ Replace patterns in footer before saving """
        text = self.footer_text
        text = text.replace('%(company)s', self.company_id.name)
        text = text.replace('%(internal_reference)s', self.name)
        text = text.replace('%(customer_reference)s', self.reference_auto)
        text = text.replace('%(customer_name)s', self.partner_id.name)
        text = text.replace('%(salesman)s', self.user_id.name)
        bank_account_ids = self.env['account.journal'].search([
            ('company_id', '=', self.env.user.company_id.id),
            ('bank_acc_number', '!=', '')])
        if len(bank_account_ids) > 0:
            if len(bank_account_ids) > 1:
                bank_account_ids = bank_account_ids[0]
            text = text.replace('%(bank_number)s', bank_account_ids.bank_acc_number)
        self.footer_text_replaced = text
        return text.encode('utf-8')

    @api.model
    def get_bank_account(self):
        """  Deduce bank account from default journal entry (for reporting purpose) """
        bank_account_ids = self.env['account.journal'].search([
            ('company_id', '=', self.env.user.company_id.id),
            ('bank_acc_number', '!=', '')])
        if len(bank_account_ids) >= 1:
            if len(bank_account_ids) > 1:
                bank_account_ids = bank_account_ids[0]
            return "%s : IBAN %s - %s " \
                   % str(bank_account_ids.bank_id.name),\
                   str(bank_account_ids.bank_acc_number),\
                   str(bank_account_ids.bank_id.bic)

    @api.model
    def get_used_taxes(self):
        """ Deduce tax to apply base on SOL """
        used_taxes = ''
        for line in self.order_line:
            for tax in line.tax_id:
                if tax.name not in used_taxes:
                    if len(used_taxes) > 0:
                        used_taxes = used_taxes + ", " + tax.name
                    else:
                        used_taxes = tax.name
        return used_taxes

    @api.depends('order_line')
    @api.onchange('order_line.price_unit')
    def update_total(self):
        """ Hack to trigger total amount display change before save """
        self._amount_all()
