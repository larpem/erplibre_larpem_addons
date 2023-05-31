import datetime

from odoo import SUPERUSER_ID, _, api, fields, models


def migrate(cr, version):
    # Always apply to correct data
    # if not version:
    #     return
    # Version 12.0.2.0 add model larpem.banque.transaction
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Transfert total to transaction
        banque_compte_ids = env["larpem.banque.compte"].search([])
        for compte in banque_compte_ids:
            value = {
                "montant": compte.total,
                "destination_compte": compte.id,
                "date_transaction": datetime.datetime(2022, 10, 1, 22),
            }
            env["larpem.banque.transaction"].create(value)

            # Compute all name, algorith change
            compte._compute_name()
            compte._compute_total()
