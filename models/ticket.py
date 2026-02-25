from odoo import models, fields, api

class ITTicket(models.Model):
    _name = 'it.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    ticket_type = fields.Selection([
        ('incident', 'Incident (Break/Fix)'),
        ('request', 'Service Request (New Asset)'),
        ('inquiry', 'General Inquiry / Help')
    ], string="Request Type", default='incident', required=True)


    state = fields.Selection([
        ('draft', 'New'),
        ('assigned', 'Assigned'),
        ('in_progress', 'Work in Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', tracking=True)


    created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    assigned_to = fields.Many2one('res.users', string="IT Support")

# Satisfaction Rating (Only visible when Closed)
    satisfaction_rate = fields.Selection([
        ('1', 'Dissatisfied'),
        ('2', 'Neutral'),
        ('3', 'Satisfied'),
        ('4', 'Very Satisfied')
    ], string="Satisfaction", tracking=True)

# if the current user has the 'it_support' group, they can see the assigned tickets and change their state
    def action_assign_to_me(self):
        for record in self:
            record.assigned_to = self.env.user
            record.state = 'assigned'

    def action_close_ticket(self):
        for record in self:
            record.state = 'closed'