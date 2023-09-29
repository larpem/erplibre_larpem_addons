from odoo import _, api, fields, models


class LarpemRestoRepas(models.Model):
    _name = "larpem.resto.repas"
    _description = "Restaurant LARPEM"

    name = fields.Char(string="Repas", help="Repas fait.")

    active = fields.Boolean(default=True)

    price = fields.Float(string="Prix")
