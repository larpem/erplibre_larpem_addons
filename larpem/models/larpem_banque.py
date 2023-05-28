from odoo import _, api, fields, models


class LarpemBanque(models.Model):
    _name = "larpem.banque"
    _description = "Banque"

    name = fields.Char()

    description = fields.Char()
