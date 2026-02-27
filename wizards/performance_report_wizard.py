from odoo import models, fields, api
from datetime import datetime, time
import logging

_logger = logging.getLogger(__name__)


class ITPerformanceWizard(models.TransientModel):
    _name = 'it.performance.report.wizard'
    _description = 'IT Support Performance Wizard'

    date_from = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    date_to = fields.Date(string="End Date", required=True, default=fields.Date.context_today)

    def action_print_report(self):
        # ✅ Just pass self, no data dict needed
        return self.env.ref('it_ticket.it_performance_report_action').report_action(self)


class ReportITPerformance(models.AbstractModel):
    _name = 'report.it_ticket.report_performance_template'
    _description = 'IT Performance Report Logic'

    @api.model
    def _get_report_values(self, docids, data=None):
        _logger.warning(">>> _get_report_values CALLED — docids: %s", docids)

        wizard = self.env['it.performance.report.wizard'].browse(docids)

        if not wizard:
            _logger.warning(">>> wizard is empty!")
            return {
                'doc_ids': docids,
                'doc_model': 'it.performance.report.wizard',
                'docs': wizard,
                'doc': wizard,
                'performance_data': [],
            }

        doc = wizard[0]
        _logger.warning(">>> date_from: %s | date_to: %s", doc.date_from, doc.date_to)

        # ✅ Fetch all tickets without date filter first to confirm data exists
        # ✅ UTC-safe date range
        start_dt = fields.Datetime.from_string(str(doc.date_from) + ' 00:00:00')
        end_dt = fields.Datetime.from_string(str(doc.date_to) + ' 23:59:59')

        tickets = self.env['it.ticket'].search([
            ('create_date', '>=', start_dt),
            ('create_date', '<=', end_dt),
        ])
        _logger.warning(">>> Total tickets found: %s", len(tickets))

        for t in tickets:
            _logger.warning(">>> Ticket: %s | create_date: %s | assigned_to: %s | state: %s",
                t.name, t.create_date, t.assigned_to.name if t.assigned_to else 'NONE', t.state)

        performance_data = []
        users = tickets.mapped('assigned_to')
        _logger.warning(">>> Users found: %s", users.mapped('name'))

        for user in users:
            user_tickets = tickets.filtered(lambda t: t.assigned_to == user)
            performance_data.append({
                'name': user.name,
                'closed': len(user_tickets.filtered(lambda t: t.state == 'closed')),
                'cancelled': len(user_tickets.filtered(lambda t: t.state == 'cancelled')),
                'open': len(user_tickets.filtered(lambda t: t.state not in ['closed', 'cancelled'])),
                'satisfied': len(user_tickets.filtered(lambda t: t.satisfaction_rate == '4')),
            })

        _logger.warning(">>> performance_data: %s", performance_data)

        return {
            'doc_ids': docids,
            'doc_model': 'it.performance.report.wizard',
            'docs': wizard,
            'doc': doc,
            'performance_data': performance_data,
        }