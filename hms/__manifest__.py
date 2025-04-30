{
    'name': 'My Hospital',
    'author': '',
    'version': '1.0',
    'summary': 'my care hospital',
    'description': '',
    'category': '',
    'depends': ['base','crm'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/doctor_views.xml',
        'views/department_views.xml',
        'views/patient_views.xml',
         'views/res_partner_view.xml',
        #'views/patient_log_view.xml',
        'reports/patient_report.xml',
        'reports/patient_template.xml',
        'views/menu.xml',
    ],
    'application': True
}
