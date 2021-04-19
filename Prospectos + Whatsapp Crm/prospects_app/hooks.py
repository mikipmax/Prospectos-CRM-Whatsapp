from odoo import api, fields, tools


def import_csv_data(cr, registry):
    """
    Method that allows loading by default one or more of a csv file made up
    of the respective data of a module each time it is installed, it is
    also configured so that each time the module is updated, the data is
    not reloaded, if not only the first time of installation.
    """
    files = ['data/sc.info.csv']
    for file in files:
        tools.convert_file(cr, 'prospects_app', file, None,
                           mode='init', noupdate=True, kind='init')


def post_init(cr, registry):
    """
    This method originates from odoo, and allows us to intercept and
    perform operations during the installation of a module.
    """
    import_csv_data(cr, registry)
