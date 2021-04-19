from odoo import fields, models


class Messages(models.TransientModel):
    """
    Class that represents the necessary fields to send a WhatsApp message
    through its own API.
    """
    _name = "sc.messages"
    _description = "Messages to the user"
    name = fields.Char("Message type", readonly=True)
    message = fields.Char("Message", readonly=True)
    sent = fields.Integer("Sent", readonly=True)
    not_sent = fields.Integer("Not sent", readonly=True)
    validation_message = fields.Html("Validation Message", readonly=True)
