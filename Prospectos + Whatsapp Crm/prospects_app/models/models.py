from odoo import fields, models, _, api
from odoo.exceptions import ValidationError
from datetime import datetime


class Prospects(models.Model):
    """
    Class that maps each of the columns that come in the excel file that is
    obtained through the superintendent of companies.
    """
    _name = "sc.info"
    _description = "Prospects Data"
    _inherit = "mail.thread"

    name = fields.Char("Company", track_visibility="onchange")
    year = fields.Char("Year", track_visibility="onchange")
    registration_date = fields.Datetime("Registration Date",
                                        track_visibility="onchange")
    intendancy = fields.Char("Intendancy", track_visibility="onchange")
    ruc = fields.Char("RUC", track_visibility="onchange")
    constitution_date = fields.Datetime("Constitution Date",
                                        track_visibility="onchange")
    legal_representative = fields.Char("Legal Representative",
                                       track_visibility="onchange")
    company_type = fields.Char("Company Type", track_visibility="onchange")
    legal_status = fields.Char("Legal Status", track_visibility="onchange")
    legal_act = fields.Char("Legal Act", track_visibility="onchange")
    region = fields.Char("Region", track_visibility="onchange")
    province = fields.Char("Province", track_visibility="onchange")
    canton = fields.Char("Canton", track_visibility="onchange")
    city = fields.Char("City", track_visibility="onchange")
    street = fields.Char("Street", track_visibility="onchange")
    house_no = fields.Char("House No.", track_visibility="onchange")
    intersection = fields.Char("Intersection", track_visibility="onchange")
    edifice = fields.Char("Edifice", track_visibility="onchange")
    neighborhood = fields.Char("Neighborhood", track_visibility="onchange")
    phone = fields.Char("Phone", track_visibility="onchange")
    email = fields.Char("Email", track_visibility="onchange")
    activity_field = fields.Char("Activity field", track_visibility="onchange")
    description_field = fields.Char("Description(Field)",
                                    track_visibility="onchange")
    ciiu = fields.Char("CIIU", track_visibility="onchange")
    description_ciiu = fields.Char("Description(CIIU)",
                                   track_visibility="onchange")
    admision_date_legal_act = fields.Datetime("Admission date(Legal Act)",
                                              track_visibility="onchange")
    legal_act_capital = fields.Float("Legal Act Capital",
                                    track_visibility="onchange")
    constitution_type = fields.Char("Constitution type",
                                         track_visibility="onchange")
    sending_status = fields.Selection(selection=[("not_sent", "Not sent"),
                                                 ("sent", "Sent")],
                                      string="Sending status",
                                      default="not_sent",
                                      track_visibility="onchange")

    id_reference_crm = fields.Integer("Id de crm.lead",
                                      track_visibility="onchange")

    @api.model
    def create(self, vals):
        """
        Overwriting the create method, a new functionality is added which
        consists of converting the year field of the text type excel to a date
        in order to filter by day, month or year.
        """
        year = vals.get("year", "")
        if year is not False:
            year_not_spaces = ''.join(year.split())
            if len(year_not_spaces) == 7:
                year_not_spaces = year_not_spaces + "-" + "02"
                vals["registration_date"] = datetime.strptime(year_not_spaces,
                                                              "%Y-%m-%d")
        return super(Prospects, self).create(vals)

    def action_prospects_leads(self):
        """
        Method that allows you to send information from the prospects module to
        the crm.lead module. Here we carry out a pre-processing of the data, we
        remove blank spaces, we validate that there is a Ruc to send the
        information, we also validate the phone or cell number.
        """
        mobile = ""
        phone = ""
        pais = self.env['res.country'].search([('code', '=', 'EC')])  #

        message = ""
        message_validation = ""

        sent = 0
        not_sent = 0
        for rec in self:

            if rec.sending_status == "not_sent":
                if rec.name is False:
                    rec.name = ""
                if rec.ruc is not False:
                    if rec.phone is not False:
                        rec.phone = ''.join(rec.phone.split())
                        if len(rec.phone) <= 9:
                            mobile = "+593"
                            phone = rec.phone
                        else:
                            mobile = "+593" + rec.phone[1:]
                            phone = ""
                    vals = {
                        'name': rec.ruc,
                        'partner_name': rec.name,
                        'city': rec.city,
                        'street': rec.street,
                        'street2': rec.intersection,
                        'country_id': pais.id,
                        'phone': phone,
                        'mobile': mobile,
                        'contact_name': rec.legal_representative,
                        'email_from': rec.email,
                    }
                    id_reference_crm = self.env['crm.lead'].sudo().create(vals)

                    rec.update({
                        "sending_status": "sent",
                        "id_reference_crm": id_reference_crm
                    })

                    sent += 1
                else:
                    message_validation += "There's no Ruc to: " + rec.name \
                                          + ".<br>"
                    not_sent += 1
            else:
                message_validation += "It already exists in Leads " \
                                      + rec.name + ".<br>"
                not_sent += 1

            if sent > 0:
                message = "Successfully saved log(s)"

        return {'type': 'ir.actions.act_window',
                'name': _('Info'),
                'res_model': 'sc.messages',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_message': message,
                            'default_sent': sent,
                            'default_message_validation': message_validation,
                            'default_not_sent': not_sent},

                }


class ResProspects(models.Model):
    """
    Class that inherits from crm.leads, this in order to override the
    delete method, so that, every time a record is deleted from crm.leads,
    in our module it is put as a record not sent, in case you want to
    resend said record later.
    """
    _inherit = "crm.lead"

    company_type = fields.Char("Company Type")

    def unlink(self):

        ids = []
        for i in self:
            ids.append(i.id)

        prospects = self.env['sc.info'].sudo().search(
            [('id_reference_crm', 'in', ids)], limit=None)
        for prospect in prospects:
            prospect.update({
                "sending_status": "not_sent",
                "id_reference_crm": 0

            })
        return super(ResProspects, self).unlink()
