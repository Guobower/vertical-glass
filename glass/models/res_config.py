from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class sale_glass_company_config_setting_check_config(models.Model):
    # ----- MODEL NAME
    _name = 'glass.sale.config.settings.data'

    # ----- MODEL FIELDS
    default_header_text = fields.Html('Default header text')
    default_footer_text = fields.Html('Default footer text')
    
    installation_product_id = fields.Many2one('product.product', 'Product for Installation')
    moving_product_id = fields.Many2one('product.product', 'Product for Moving')
    km_product_id = fields.Many2one('product.product', 'Product for KM')

class sale_glass_company_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'glass.sale.config.settings'

    default_header_text = fields.Html('Default header text')
    default_footer_text = fields.Html('Default footer text')
    
    installation_product_id = fields.Many2one('product.product', 'Product for Installation')
    moving_product_id = fields.Many2one('product.product', 'Product for Moving')
    km_product_id = fields.Many2one('product.product', 'Product for KM')

    installation_price = fields.Float('Installation Price', related='installation_product_id.list_price')
    moving_price = fields.Float('Moving Price', related='moving_product_id.list_price')
    km_price = fields.Float('KM Price', related='km_product_id.list_price')

    @api.model
    def get_default_glass_sale_config_settings_values(self, fields):
        setting = self.env['glass.sale.config.settings.data'].search([])
        if setting:
            return {
                'default_header_text': setting.default_header_text,
                'default_footer_text': setting.default_footer_text,

                'installation_product_id': setting.installation_product_id.id,
                'moving_product_id': setting.moving_product_id.id,
                'km_product_id': setting.km_product_id.id,
            }

    @api.one
    def set_default_glass_sale_config_settings_values(self):
        setting = self.env['glass.sale.config.settings.data'].search([])
        if setting:
            setting.default_header_text = self.default_header_text
            setting.default_footer_text = self.default_footer_text

            setting.installation_product_id = self.installation_product_id
            setting.moving_product_id = self.moving_product_id
            setting.km_product_id = self.km_product_id
