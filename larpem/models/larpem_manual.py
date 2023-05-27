from odoo import _, api, fields, models


class LarpemManual(models.Model):
    _name = "larpem.manual"
    _description = "Manuel utilisateur et administrateur"

    name = fields.Char(
        compute="_compute_name",
        store=True,
    )

    parent_id = fields.Many2one(
        comodel_name="larpem.manual",
        string="Parent",
    )

    enfant_id = fields.One2many(
        comodel_name="larpem.manual",
        inverse_name="parent_id",
        string="Enfant",
    )

    admin = fields.Boolean(
        string="Admin seulement",
        help="Cette information est seulement pour les organisateurs du jeu.",
    )

    key = fields.Char()

    title = fields.Char()

    title_html = fields.Html()

    description = fields.Text()

    bullet_description = fields.Char()

    second_bullet_description = fields.Char()

    under_level_color = fields.Char()

    sub_key = fields.Char()

    model = fields.Char()

    point = fields.Char()

    hide_player = fields.Boolean()

    @api.depends("title")
    def _compute_name(self):
        for rec in self:
            if rec.title:
                rec.name = rec.title
            else:
                rec.name = "NO TITLE"
