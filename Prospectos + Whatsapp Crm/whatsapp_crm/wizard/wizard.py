from odoo import models, api, fields


class WhatsappSendMessage(models.TransientModel):
    """
    Class that represents the body of the whatsapp message.
    """
    _name = 'whatsapp.message.wizard'

    user_id = fields.Char("Recipient")
    mobile = fields.Char("Mobile", required=True)
    message = fields.Text(string="Message", required=True)

    def send_message(self):
        """
        Necessary method to send the message through the whatsapp API.
        """
        if self.message and self.mobile:
            message_string = ''
            message = self.message.split(' ')
            for msg in message:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone=" + self.mobile
                       + "&text=" + message_string,
                'target': 'new',
                'res_id': self.id,
            }
