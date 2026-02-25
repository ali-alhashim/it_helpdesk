from odoo import models, fields, api

class ITTicket(models.Model):
    _name = 'it.helpdesk.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    category = fields.Selection([
        ('buy', 'Buying Devices'),
        ('fix', 'Fixing Device'),
        ('help', 'Task Help')
    ], string="Category", required=True)


    status = fields.Selection([
        ('new', 'New'),
        ('process', 'In Progress'),
        ('closed', 'Closed')
    ], default='new', tracking=True)


    created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    assigned_to = fields.Many2one('res.users', string="IT Support")

    rating = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Average'),
        ('3', 'Good'),
        ('4', 'Excellent')
    ], string="Satisfaction Rating")