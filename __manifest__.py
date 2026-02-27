{
    'name': 'IT Ticket Management',
    'version': '1.0',
    'category': 'Operations/IT',
    'summary': 'Manage Ticket tracking and assignments for IT support',
    'author': 'Ali Alhashim',
    'depends': ['base', 'hr', 'mail', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/performance_report_wizard_view.xml',
        'wizards/performance_report_templates.xml',
        'views/tickets_views.xml',
       
        
    ],
   
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}