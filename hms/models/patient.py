from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'

    first_name = fields.Char('First Name', required=True)
    last_name = fields.Char('Last Name', required=True)
    birth_date = fields.Date('Birth Date')
    history = fields.Html('History')
    cr_ratio = fields.Float('CR Ratio')
    blood_type = fields.Selection([('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], string='Blood Type')
    pcr = fields.Boolean('PCR')
    image = fields.Image('Image')
    address = fields.Text('Address')
    age = fields.Integer('Age',compute='_compute_age', store=True)
    email = fields.Char('Email', unique=True)

    department_id = fields.Many2one('hms.department', 'Department')
    doctor_ids = fields.Many2many('hms.doctors', string='Doctors')
    log_history_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log History')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = fields.Date.today()
                rec.age = today.year - rec.birth_date.year
            else:
                rec.age = 0  
    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR has been automatically checked due to the age being less than 30.'
                }
            }
        if self.age < 50:
            self.history = False

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        if self.pcr and not self.cr_ratio:
            raise ValidationError('CR Ratio is mandatory when PCR is checked.')

    @api.model
    def create(self, vals):
        record = super(Patient, self).create(vals)
        record._create_log('Patient record created')
        return record

    def _create_log(self, description):
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': description,
            'created_by': self.env.user.id,
            'date': fields.Datetime.now(),
        })


    @api.constrains('email')
    def _check_email(self):
        if self.email:
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, self.email):
                raise ValidationError('Invalid email format.')
