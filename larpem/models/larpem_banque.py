from odoo import _, api, fields, models


class LarpemBanque(models.Model):
    _name = "larpem.banque"
    _inherit = "portal.mixin"
    _description = "Banque"

    name = fields.Char()

    description = fields.Char()

    def _compute_access_url(self):
        super(LarpemBanque, self)._compute_access_url()
        for larpem_banque in self:
            larpem_banque.access_url = (
                "/my/larpem_banque/%s" % larpem_banque.id
            )
