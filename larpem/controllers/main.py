from odoo import http
from odoo.http import request


class LarpemController(http.Controller):
    @http.route(
        ["/larpem/larpem_manual/<int:larpem_manual>"],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_larpem_manual(self, larpem_manual=None):
        env = request.env(context=dict(request.env.context))

        larpem_manual_cls = env["larpem.manual"]
        if larpem_manual:
            larpem_manual_id = (
                larpem_manual_cls.sudo().browse(larpem_manual).exists()
            )
        else:
            larpem_manual_id = None
        dct_value = {"larpem_manual_id": larpem_manual_id}

        # Render page
        return request.render(
            "larpem.larpem_manual_unit_larpem_manual", dct_value
        )

    @http.route(
        ["/larpem/larpem_manual_list"],
        type="json",
        auth="public",
        website=True,
    )
    def get_larpem_manual_list(self):
        env = request.env(context=dict(request.env.context))

        larpem_manual_cls = env["larpem.manual"]
        larpem_manual_ids = larpem_manual_cls.sudo().search([]).ids
        larpem_manual_s = larpem_manual_cls.sudo().browse(larpem_manual_ids)

        dct_value = {"larpem_manual_s": larpem_manual_s}

        # Render page
        return request.env["ir.ui.view"].render_template(
            "larpem.larpem_manual_list_larpem_manual", dct_value
        )
