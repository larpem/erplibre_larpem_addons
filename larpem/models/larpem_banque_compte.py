from odoo import _, api, fields, models


class LarpemBanqueCompte(models.Model):
    _name = "larpem.banque.compte"
    _description = "Compte bancaire"

    name = fields.Char(
        compute="_compute_name",
        store=True,
    )

    no_compte = fields.Char(string="Numéro de compte")

    banque_id = fields.Many2one(
        comodel_name="larpem.banque",
        string="Banque",
    )

    personnage_id = fields.Many2one(
        comodel_name="larpem.personnage",
        string="Personnage",
    )

    total = fields.Float(string="Sommaire du compte")

    @api.depends("banque_id", "personnage_id")
    def _compute_name(self):
        for r in self:
            r.name = f"{r.banque_id.name} - {r.personnage_id.name}"
