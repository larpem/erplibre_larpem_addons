from odoo import SUPERUSER_ID, _, api, fields, models


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # GOAL, detach data from module to don't be delete
        lst_model_to_keep = ["larpem.banque.compte", "larpem.banque"]
        for model in lst_model_to_keep:
            data_ids = env["ir.model.data"].search([("model", "=", model)])
            if data_ids.exists():
                data_ids.unlink()
