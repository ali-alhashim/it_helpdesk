from odoo import models, fields, api

class ITPerformanceWizard(models.TransientModel):
    _name = 'it.performance.report.wizard'
    _description = 'IT Support Performance Wizard'

    date_from = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    date_to = fields.Date(string="End Date", required=True, default=fields.Date.context_today)

    def action_print_report(self):
        # We search for the data here or pass the dates to the report
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        # 'it_performance_report_action' is the XML ID of the report action defined in the module
        return self.env.ref('it_ticket.it_performance_report_action').report_action(self, data=data)
    



class ReportITPerformance(models.AbstractModel):
    _name = 'report.it_ticket.report_performance_template'
    _description = 'IT Performance Report Logic'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['it.performance.report.wizard'].browse(docids)
        
        # 1. Fetch all tickets in date range
        tickets = self.env['it.ticket'].search([
            ('create_date', '>=', docs.date_from),
            ('create_date', '<=', docs.date_to)
        ])

        # 2. Group data by Support User
        performance_data = []
        users = tickets.mapped('assigned_to')

        for user in users:
            user_tickets = tickets.filtered(lambda t: t.assigned_to == user)
            performance_data.append({
                'name': user.name,
                'closed': len(user_tickets.filtered(lambda t: t.stage_id.name == 'closed')), # Adjust stage names
                'cancelled': len(user_tickets.filtered(lambda t: t.stage_id.name == 'cancelled')),
                'open': len(user_tickets.filtered(lambda t: t.stage_id.name not in ['closed', 'cancelled'])),
                'satisfied': len(user_tickets.filtered(lambda t: t.rating == '4')), # Adjust based on your rating field
            })

        return {
            'doc_ids': docids,
            'doc_model': 'it.performance.report.wizard',
            'docs': docs,
            'doc': docs,
            'performance_data': performance_data,
        }