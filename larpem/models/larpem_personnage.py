from odoo import _, api, fields, models


class LarpemPersonnage(models.Model):
    _name = "larpem.personnage"
    _description = "Personnage"

    name = fields.Char(
        compute="_compute_name",
        store=True,
    )

    nom_personnage = fields.Char()

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Participant",
    )

    compte_bancaire_ids = fields.One2many(
        comodel_name="larpem.banque.compte",
        inverse_name="personnage_id",
        string="Comptes bancaires",
    )

    @api.depends("nom_personnage", "partner_id")
    def _compute_name(self):
        for rec in self:
            name = ""
            if rec.nom_personnage:
                name = rec.nom_personnage
            if rec.partner_id and rec.partner_id.name:
                if name:
                    name += " - "
                name += rec.partner_id.name
            rec.name = name
