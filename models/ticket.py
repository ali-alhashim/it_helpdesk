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


    created_by = fields.Many2one('res.users', default=lambda self: self.env.user, string="Created By", readonly=True)
    assigned_to = fields.Many2one('res.users', string="IT Support")

# Satisfaction Rating (Only visible when Closed)
    satisfaction_rate = fields.Selection([
        ('1', 'Dissatisfied'),
        ('2', 'Neutral'),
        ('3', 'Satisfied'),
        ('4', 'Very Satisfied')
    ], string="Satisfaction", tracking=True)

    is_rated = fields.Boolean(string="Already Rated", default=False, copy=False)

    is_creator = fields.Boolean(compute='_compute_is_creator')


    @api.depends('created_by')
    def _compute_is_creator(self):
        for rec in self:
            rec.is_creator = (rec.created_by.id == self.env.user.id)


    def write(self, vals):
        if 'satisfaction_rate' in vals:
            for rec in self:
                if rec.created_by.id != self.env.user.id:
                    raise UserError(_("Only the ticket creator can rate satisfaction."))
                if rec.is_rated:
                    raise UserError(_("You have already rated this ticket and cannot change it."))
                if rec.state not in ('resolved', 'closed'):
                    raise UserError(_("You can only rate resolved or closed tickets."))
            vals['is_rated'] = True
        return super().write(vals)

    

           

    def action_close_ticket(self):
        for record in self:
            record.state = 'closed'


    def action_assign(self):
        # if the current user has the 'group_it_ticket_support' group, they can see the assigned tickets and change their state
        for record in self:
            if not self.env.user.has_group('it_ticket.group_it_ticket_support'):
                raise UserError(_("Only IT Support staff can assign tickets."))
            record.write({
                'state': 'assigned',
                'assigned_to': self.env.user.id
            })
        

    def action_progress(self):
        self.write({'state': 'in_progress'})

    def action_resolve(self):
        self.write({'state': 'resolved'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})