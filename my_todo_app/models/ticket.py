from odoo import models, fields


class Ticket(models.Model):
    _name = 'lr.ticket'
    _description = 'ticket'
    # _log_access = False

    name = fields.Char()
    number = fields.Integer()
    tag = fields.Char()
    description = fields.Text()
    file = fields.Binary()
    state = fields.Selection([('new', 'New'),('doing', 'Doing'),('done', 'Done')], default='new')
