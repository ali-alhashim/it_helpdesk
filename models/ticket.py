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
            # Security check: only IT support can assign
            if not self.env.user.has_group('it_helpdesk.group_it_support'):
                raise UserError(_("Only IT Support staff can assign tickets."))
            else:
                 record.assigned_to = self.env.user
                 record.state = 'assigned'

           

    def action_close_ticket(self):
        for record in self:
            record.state = 'closed'


    def action_assign(self):
        self.write({'state': 'assigned', 'assigned_to': self.env.user.id})

    def action_progress(self):
        self.write({'state': 'in_progress'})

    def action_resolve(self):
        self.write({'state': 'resolved'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})