from odoo import _, api, fields, models


class LarpemManual(models.Model):
    _name = "larpem.manual"
    _description = "Manuel utilisateur et administrateur"

    name = fields.Char()

    level = fields.Integer()

    admin = fields.Boolean(
        string="Admin seulement",
        help="Cette information est seulement pour les organisateurs du jeu.",
    )

    key = fields.Char()

    title = fields.Char()

    description = fields.Char()

    bullet_description = fields.Char()

    second_bullet_description = fields.Char()

    under_level_color = fields.Char()

    sub_key = fields.Char()

    model = fields.Char()

    point = fields.Char()

    hide_player = fields.Boolean()
