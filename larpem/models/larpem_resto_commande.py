from odoo import _, api, fields, models


class LarpemRestoCommande(models.Model):
    _name = "larpem.resto.commande"
    _description = "Restaurant LARPEM"

    # TODO support merge

    name = fields.Many2one(
        comodel_name='larpem.personnage', string="Identifiant commande", help="Mot pour reconnaître le client.")

    no_commande = fields.Integer(string="# de commande", help="Chiffre de la commande", )

    # TODO mettre default modifiable
    zone_repas = fields.Selection(
        selection=[("Vendredi soir", "Vendredi soir"), ("Samedi matin", "Samedi matin"), ("Samedi soir", "Samedi soir")],
        required=True,
        default="Samedi soir",
    )

    repas = fields.Many2many(comodel_name="larpem.resto.repas")

    type = fields.Selection(
        selection=[("Payé", "Payé"), ("Employé", "Employé"),
                   ("Admin", "Admin"), ("+ didney", "+ didney"), ("Spécial", "Spécial")],
    )
    #
    # category_paiement = fields.Selection(
    #     selection=[("Attribut", "Attribut"), ("Ressource", "Ressource")],
    #     required=True,
    #     default="ressource",
    # )

    paye = fields.Boolean(string="Est payé", help="La commande est payée.")

    commande_recu = fields.Boolean(string="Commande reçu", help="La commande a été réceptionné par le client.")

    description_paiement = fields.Char(string="Description du paiement", help="Que contient le paiement")
