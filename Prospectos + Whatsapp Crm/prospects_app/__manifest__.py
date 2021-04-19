{
    "name": "Prospects",
    "summary": "Application that manages public data of superintendency of companies",
    "description":"""
    Prospects is a module focused on importing data from the superintendency of 
    companies, through the use of csv or xlsx files, once the data is loaded, it
    can be managed, so that the user has the facility to send the records from 
    each company to the CRM LEADS module.
    This module also has multiple types of views, plus many filters and 
    groupings.
    """,
    "author": "PG",
    "version": "1.0",
    'post_init_hook': 'post_init',
    "depends": ['base', 'crm', 'mail'],
    "data": ["views/views.xml", "views/messages.xml",
             "security/ir_model_access.xml"
             ],
}