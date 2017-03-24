from openerp import models, fields, api, _


import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    repair_order_id = fields.Many2one('repair.order', string="Repair Order")