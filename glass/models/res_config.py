# -*- coding: utf-8 -*-
"""
Extension to res.config.setting allowing to manage glass product settings
"""
import logging
from openerp import models, fields, api, _
_logger = logging.getLogger(__name__)


class SaleGlassCompanyConfigSettingCheckConfig(models.Model):
    """ Main class checker """
    _name = 'glass.sale.config.settings.data'
    # ----- MODEL FIELDS
    company_id = fields.Many2one('res.company', 'Company')

    default_header_text = fields.Html()
    default_footer_text = fields.Html()

    installation_product_id = fields.Many2one('product.product', 'Product for Installation')
    moving_product_id = fields.Many2one('product.product', 'Product for Moving')
    km_product_id = fields.Many2one('product.product', 'Product for KM')

    installation_price = fields.Float(related='installation_product_id.list_price')
    moving_price = fields.Float(related='moving_product_id.list_price')
    km_price = fields.Float('KM Price', related='km_product_id.list_price')

    glass_maximum_area_warning = fields.Text('Glass Max. Area Warning')


class SaleGlassCompanyConfigSettings(models.TransientModel):
    """ Main class """
    _inherit = 'res.config.settings'
    _name = 'glass.sale.config.settings'

    company_id = fields.Many2one('res.company', 'Company', required=True)

    default_header_text = fields.Html()
    default_footer_text = fields.Html()

    installation_product_id = fields.Many2one('product.product', 'Product for Installation')
    moving_product_id = fields.Many2one('product.product', 'Product for Moving')
    km_product_id = fields.Many2one('product.product', 'Product for KM')

    installation_price = fields.Float(related='installation_product_id.list_price')
    moving_price = fields.Float(related='moving_product_id.list_price')
    km_price = fields.Float('KM Price', related='km_product_id.list_price')

    glass_maximum_area_warning = fields.Text('Glass Max. Area Warning')

    available_variables = fields.Text('Variables', default='Available variables: \n'
                                                           ' %(company)s : company name \n'
                                                           ' %(internal_reference)s : your order number\n'
                                                           ' %(customer_reference)s : customer order number\n'
                                                           ' %(customer_name)s : customer name\n'
                                                           ' %(salesman)s : salesman\n'
                                                           ' %(bank_number)s : company first bank account number')

    @api.model
    def get_default_gscs_values(self, fields):
        """ loads new settings
         pylint: a method name can not exceed 30 chars so get_default_glass_sale_config_settings_values is forbidden
         pylint: api.models decorator makes passing fields as second param mandatory. This triggers an obvious lint
         error.
         """
        setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
        if setting:
            return {
                'company_id': setting.company_id.id,
                'default_header_text': setting.default_header_text,
                'default_footer_text': setting.default_footer_text,

                'installation_product_id': setting.installation_product_id.id,
                'moving_product_id': setting.moving_product_id.id,
                'km_product_id': setting.km_product_id.id,

                'installation_price': setting.installation_price,
                'moving_price': setting.moving_price,
                'km_price': setting.km_price,

                'glass_maximum_area_warning': setting.glass_maximum_area_warning,
            }
        else:
            new_setting = self.env['glass.sale.config.settings.data'].create(
                {
                    'company_id': self.env.user.company_id.id,
                })
            return {
                'company_id': new_setting.company_id.id,
            }

    @api.one
    def set_default_gscs_values(self):
        """
        set default setting for glass products SO
        pylint: a method name can not exceed 30 chars so set_default_glass_sale_config_settings_values is forbidden
        """
        setting = self.env['glass.sale.config.settings.data'].search([('company_id', '=', self.env.user.company_id.id)])
        if setting:
            setting.company_id = self.company_id
            setting.default_header_text = self.default_header_text
            setting.default_footer_text = self.default_footer_text

            setting.installation_product_id = self.installation_product_id
            setting.moving_product_id = self.moving_product_id
            setting.km_product_id = self.km_product_id

            setting.installation_price = self.installation_price
            setting.moving_price = self.moving_price
            setting.km_price = self.km_price

            setting.glass_maximum_area_warning = self.glass_maximum_area_warning
