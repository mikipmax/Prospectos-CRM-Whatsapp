{
    'name': 'WhatsApp Crm Leads',
    'version': '14.0.1',
    'summary': 'Sending messages from odoo (crm.lead) through WhatsApp web',
    'description': 'Sending messages from odoo (crm.lead) through WhatsApp web',

    'category': 'Extra Tools',
    'author': 'PG',
    'maintainer': 'PG',

    'depends': [
        'base', 'contacts', 'crm'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'wizard/wizard.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False
}
