from odoo import http
from odoo.http import request


class LarpemController(http.Controller):
    @http.route(
        ["/larpem/larpem_manuel/<int:larpem_manuel>"],
        type="http",
        auth="public",
        website=True,
    )
    def get_page_larpem_manuel(self, larpem_manuel=None):
        env = request.env(context=dict(request.env.context))

        larpem_manuel_cls = env["larpem.manuel"]
        if larpem_manuel:
            larpem_manuel_id = (
                larpem_manuel_cls.sudo().browse(larpem_manuel).exists()
            )
        else:
            larpem_manuel_id = None
        dct_value = {"larpem_manuel_id": larpem_manuel_id}

        # Render page
        return request.render(
            "larpem.larpem_manuel_unit_larpem_manuel", dct_value
        )

    @http.route(
        ["/larpem/larpem_manuel_list"],
        type="json",
        auth="public",
        website=True,
    )
    def get_larpem_manuel_list(self):
        env = request.env(context=dict(request.env.context))

        larpem_manuel_cls = env["larpem.manuel"]
        larpem_manuel_ids = larpem_manuel_cls.sudo().search([]).ids
        larpem_manuel_s = larpem_manuel_cls.sudo().browse(larpem_manuel_ids)

        dct_value = {"larpem_manuel_s": larpem_manuel_s}

        # Render page
        return request.env["ir.ui.view"].render_template(
            "larpem.larpem_manuel_list_larpem_manuel", dct_value
        )
