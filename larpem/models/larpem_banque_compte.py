from odoo import _, api, fields, models


class LarpemBanqueCompte(models.Model):
    _name = "larpem.banque.compte"
    _description = "Compte bancaire"

    name = fields.Char()

    banque_id = fields.Many2one(
        comodel_name="larpem.banque",
        string="Banque",
    )

    personnage_id = fields.Many2one(
        comodel_name="larpem.personnage",
        string="Personnage",
    )

    total = fields.Float(string="Sommaire du compte")
