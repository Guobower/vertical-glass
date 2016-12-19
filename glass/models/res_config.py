from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class sale_glass_company_config_setting_check_config(models.Model):
    # ----- MODEL NAME
    _name = 'glass.sale.config.settings.data'

    # ----- MODEL FIELDS
    company_id = fields.Many2one('res.company', 'Company')

    default_header_text = fields.Html('Default header text')
    default_footer_text = fields.Html('Default footer text')
    
    installation_product_id = fields.Many2one('product.product', 'Product for Installation')
    moving_product_id = fields.Many2one('product.product', 'Product for Moving')
    km_product_id = fields.Many2one('product.product', 'Product for KM')

    installation_price = fields.Float('Installation Price', related='installation_product_id.list_price')
    moving_price = fields.Float('Moving Price', related='moving_product_id.list_price')
    km_price = fields.Float('KM Price', related='km_product_id.list_price')

    glass_maximum_area_warning = fields.Text('Glass max. Area Warning')

class sale_glass_company_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'glass.sale.config.settings'

    company_id = fields.Many2one('res.company', 'Company', required=True)

    default_header_text = fields.Html('Default header text')
    default_footer_text = fields.Html('Default footer text')
    
    installation_product_id = fields.Many2one('product.product', 'Product for Installation')
    moving_product_id = fields.Many2one('product.product', 'Product for Moving')
    km_product_id = fields.Many2one('product.product', 'Product for KM')

    installation_price = fields.Float('Installation Price', related='installation_product_id.list_price')
    moving_price = fields.Float('Moving Price', related='moving_product_id.list_price')
    km_price = fields.Float('KM Price', related='km_product_id.list_price')

    glass_maximum_area_warning = fields.Text('Glass max. Area Warning')

    @api.model
    def get_default_glass_sale_config_settings_values(self, fields):
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
            new_setting = self.env['glass.sale.config.settings.data'].create({
                    'company_id': self.env.user.company_id.id,
                })
            return {
                'company_id': new_setting.company_id.id,
            }

    @api.one
    def set_default_glass_sale_config_settings_values(self):
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
