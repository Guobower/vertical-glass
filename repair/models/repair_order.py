from openerp import models, fields, api


import logging
_logger = logging.getLogger(__name__)

class RepairOrder(models.Model):
    _name = 'repair.order'
    _description = 'Repair Order'

    name = fields.Char(string="Name")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('invoiced', 'Invoiced'), ('cancelled', 'Cancelled')], string="State")
    date_call = fields.Date(string="Call date")

    partner_id = fields.Many2one("res.partner", string="Customer")
    partner_repair_id = fields.Many2one("res.partner", string="Repair address")

    description = fields.Text(string="Description")
    material_to_bring = fields.Text(string="Material to bring")

    technician_id = fields.Many2one("res.partner", string="Technician")

    warranty = fields.Boolean(string="Under warranty")

    work_done = fields.Text(string="Work done")
    work_to_do = fields.Text(string="Work to do")
    date_work = fields.Date(string="Work date")
    
    