from odoo import _, api, fields, models


class LarpemBanqueCompte(models.Model):
    _name = "larpem.banque.compte"
    _inherit = ["mail.activity.mixin", "mail.thread", "portal.mixin"]
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

    type_compte = fields.Selection(
        selection=[("membre", "Membre"), ("affaire", "Affaire")],
        string="Type de compte",
        required=True,
        default="membre",
    )

    etat_compte = fields.Selection(
        selection=[
            ("actif", "Actif"),
            ("ferme", "Fermé"),
            ("block", "Bloqué"),
        ],
        string="État du compte",
        required=True,
        default="actif",
    )

    raison_etat_compte = fields.Char(
        help="La raison lorsque l'état de compte est fermé ou bloqué."
    )

    nom_personnage = fields.Char(
        string="Nom personnage", related="personnage_id.name"
    )

    personnage_id = fields.Many2one(
        comodel_name="larpem.personnage",
        string="Personnage",
        help="Est la personne responsable du compte",
    )

    nom_personnage_secondaire = fields.Char(
        string="Nom personnage secondaire",
        compute="_compute_nom_personnage_secondaire",
        store=True,
    )

    personnage_secondaire_ids = fields.Many2many(
        comodel_name="larpem.personnage",
        string="Personnage secondaire",
        help="Personne secondaire responsable du compte",
    )

    transaction_source_compte = fields.One2many(
        comodel_name="larpem.banque.transaction",
        inverse_name="source_compte",
        string="Transactions crédit",
    )

    transaction_destination_compte = fields.One2many(
        comodel_name="larpem.banque.transaction",
        inverse_name="destination_compte",
        string="Transactions débit",
    )

    total = fields.Float(
        string="Sommaire du compte", store=True, compute="_compute_total"
    )

    @api.depends(
        "banque_id",
        "personnage_id",
        "no_compte",
        "transaction_source_compte",
        "transaction_destination_compte",
    )
    def _compute_name(self):
        for r in self:
            r.name = (
                f"{r.no_compte} - {r.personnage_id.name} -"
                f" {r.banque_id.name} - {r.total}"
            )

    @api.depends("transaction_source_compte", "transaction_destination_compte")
    def _compute_total(self):
        for r in self:
            r.total = sum(
                [a.montant for a in r.transaction_destination_compte]
            ) - sum([a.montant for a in r.transaction_source_compte])

    def _compute_access_url(self):
        super(LarpemBanqueCompte, self)._compute_access_url()
        for larpem_banque_compte in self:
            larpem_banque_compte.access_url = (
                "/my/larpem_banque_compte/%s" % larpem_banque_compte.id
            )

    @api.depends("personnage_secondaire_ids")
    def _compute_nom_personnage_secondaire(self):
        for r in self:
            r.nom_personnage_secondaire = " - ".join(
                [a.name for a in r.personnage_secondaire_ids]
            )
