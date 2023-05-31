import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class LarpemBanqueTransaction(models.Model):
    _name = "larpem.banque.transaction"
    _description = "Banque"

    name = fields.Char(
        compute="_compute_name",
        store=True,
    )

    montant = fields.Float()

    date_transaction = fields.Datetime(
        string="Date de la transaction",
        default=lambda self: fields.Datetime.now(),
    )

    memo = fields.Char()

    source_compte = fields.Many2one(comodel_name="larpem.banque.compte")

    destination_compte = fields.Many2one(comodel_name="larpem.banque.compte")

    @api.depends("date_transaction", "montant")
    def _compute_name(self):
        for r in self:
            event_model_name = "event.event"
            event_id = None
            if event_model_name in self.env.keys():
                # event exist!
                event_ids = self.env["event.event"].search(
                    [
                        ("date_begin", "<=", r.date_transaction),
                        ("date_end", ">=", r.date_transaction),
                    ]
                )
                if len(event_ids) > 1:
                    _logger.warning(
                        "Find more than 1 event.event for transaction date"
                        f" {r.date_transaction}. Do you have multiple event?"
                        " Choose first for larpem.banque.transaction name."
                    )
                    event_id = event_ids[0]
                elif len(event_ids) == 1:
                    event_id = event_ids
                else:
                    # Chercher entre les événements
                    print("oups")

            name = f"{r.montant}"
            if event_id and event_id.name:
                name += f" - {event_id.name}"

            r.name = name
