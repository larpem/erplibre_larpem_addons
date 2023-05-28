from odoo import _, api, fields, models


class LarpemPersonnage(models.Model):
    _name = "larpem.personnage"
    _description = "Personnage"

    name = fields.Char(string="Nom personnage")

    nom_joueur = fields.Char(
        string="Nom joueur",
        related="partner_id.name",
        store=True,
        readonly=True,
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Participant",
    )

    compte_bancaire_ids = fields.One2many(
        comodel_name="larpem.banque.compte",
        inverse_name="personnage_id",
        string="Comptes bancaires",
    )

    compte_bancaire_secondaire_ids = fields.Many2many(
        comodel_name="larpem.banque.compte",
        inverse_name="personnage_secondaire_ids",
        string="Comptes bancaires supplémentaires",
    )

    # all_name = fields.Char(string="Nom personnage") combine name + nom_joueur et mettre dans les recherches des autres vues
