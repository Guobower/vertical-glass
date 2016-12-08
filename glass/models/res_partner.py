from openerp import models, fields, api

class res_partner(models.Model):
    _inherit = ['res.partner']
    
    ref_auto = fields.Char(string="Customer Reference", compute='_compute_customer_reference')

    @api.multi
    def _compute_customer_reference(self):
        for partner in self:
            if partner.parent_id:
                partner.ref_auto = partner.parent_id.name.lower()[0:8].replace(" ", "") + "_" + partner.name.lower()[0:8].replace(" ", "")
            else:
                partner.ref_auto = partner.name.lower()[0:8].replace(" ", "")
