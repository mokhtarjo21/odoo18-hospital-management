from odoo import models, fields

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Department'

    name = fields.Char('Name', required=True)
    capacity = fields.Integer('Capacity')
    is_opened = fields.Boolean('Is Opened', default=True)
    patient_ids = fields.One2many('hms.patient', 'department_id', string='Patients')

