from openerp import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'
    
    ref_auto = fields.Char(string="Customer Reference", compute='_compute_customer_reference', store=True)
    glass_supplier = fields.Boolean(string="Glass Supplier", default=False)

    @api.depends('name')
    def _compute_customer_reference(self):
        for partner in self:
            if partner.name:
                names = partner.name.split(" ")
                if len(names) >= 2:
                    partner.ref_auto = names[0][0:7].upper() + names[1][0:3].upper()
                else:
                    partner.ref_auto = names[0][0:7].upper()
