from odoo import _, api, fields, models


class LarpemPersonnage(models.Model):
    _name = "larpem.personnage"
    _description = "Personnage"

    name = fields.Char()

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Participant",
    )

    compte_bancaire_ids = fields.One2many(
        comodel_name="larpem.banque.compte",
        inverse_name="personnage_id",
        string="Comptes bancaires",
    )
