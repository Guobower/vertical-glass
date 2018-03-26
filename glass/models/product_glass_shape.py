# -*- coding: utf-8 -*-
"""
Manage shapes (forme - FR) , they provide a multiplier on the final price
The value of said multiplier is based on the difficulty of manufacturing the shape.
"""
import logging
from openerp import models, fields, api
from openerp.tools import openerp, image_colorize, image_resize_image_big
_logger = logging.getLogger(__name__)


class GlassShape(models.Model):
    """
    Main shape class
    """
    _name = 'product.glass.shape'
    _description = 'Glass Shape'

    name = fields.Char(required=True)
    photo = fields.Binary(string="Shape image", default=lambda self: self.get_default_image())
    multiplier = fields.Float(required=True, default=1)

    @api.multi
    def name_get(self):
        """
        Custom display instead of default name
        :return:
        """
        result = []
        for record in self:
            result.append((record.id, "%s [x %s]" % (record.name, record.multiplier)))
        return result

    @classmethod
    def get_default_image(cls):
        """
        Associate an image helper to the shape
        :return:
        """
        image_path = openerp.modules.get_module_resource('glass', 'static/src/img', 'avatar.png')
        if image_path:
            image = image_colorize(open(image_path, 'rb').read())
            return image_resize_image_big(image.encode('base64'))
