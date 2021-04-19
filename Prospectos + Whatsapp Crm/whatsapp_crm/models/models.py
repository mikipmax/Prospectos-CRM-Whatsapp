from odoo import _, models


class WhatsappCrm(models.Model):
    """
    Class that inherits from crm.lead, with the purpose of embedding a button
    on the view of said module.
    """
    _inherit = 'crm.lead'

    def send_msg(self):
        """
        This method is called from the aforementioned button, and its function
        is to take the cell phone number, and a message from the crm.lead form
        to pass it to a wizard, which then through the whatsapp api will send
        the message.
        """
        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_user_id': self.partner_name,
                            'default_mobile': self.mobile},
                }
