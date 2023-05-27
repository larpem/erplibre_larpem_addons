from odoo import _, api, fields, models


class LarpemSystemPoint(models.Model):
    _name = "larpem.system_point"
    _description = "Système de pointage de LARPEM"

    name = fields.Char(string="Description")

    identifiant = fields.Char()

    explication = fields.Char(string="Explication")

    init_value = fields.Integer(string="Valeur initiale")

    min_value = fields.Integer(string="Valeur minimal")

    max_value = fields.Integer(string="Valeur maximal")

    formule = fields.Char()

    hide_value = fields.Boolean(
        string="Cache la valeur", help="TODO à définir"
    )

    required_value = fields.Boolean(string="Valeur requise")

    invisible = fields.Boolean(string="Invisible", help="TODO à définir")

    type = fields.Selection(
        [("attribut", "Attribut"), ("ressource", "Ressource")],
        default="ressource",
        required=True,
    )
