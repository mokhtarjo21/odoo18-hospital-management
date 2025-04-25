from odoo import models, fields

class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log History'

    patient_id = fields.Many2one('hms.patient', 'Patient')
    created_by = fields.Many2one('res.users', 'Created By')
    date = fields.Datetime('Date')
    description = fields.Text('Description')
