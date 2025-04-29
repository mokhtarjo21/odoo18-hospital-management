
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')
    vat = fields.Char(string="Tax ID")  

    @api.constrains('vat', 'customer_rank')
    def _check_vat_for_customers(self):
        for partner in self:
            if partner.customer_rank > 0 and not partner.vat:
                raise ValidationError("Customers must have a Tax ID.")

    @api.constrains('email')
    def _check_email_not_in_patient(self):
        for record in self:
            if record.email:
                existing_patient = self.env['hms.patient'].search([('email', '=', record.email)], limit=1)
                if existing_patient:
                    raise ValidationError("The email '%s' is already associated with a patient and cannot be used for a customer." % record.email)

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("You cannot delete a customer linked to a patient.")
        return super(ResPartner, self).unlink()