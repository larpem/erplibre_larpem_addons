from odoo import _, api, fields, models


class LarpemSystemPoint(models.Model):
    _name = "larpem.system_point"
    _description = "Système de pointage de LARPEM"

    name = fields.Char()

    description = fields.Char(string="description")

    explication = fields.Char()

    type = fields.Char()
