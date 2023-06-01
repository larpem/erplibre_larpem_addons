import base64
import logging

import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class LarpemController(http.Controller):
    @http.route("/new/larpem_banque", type="http", auth="user", website=True)
    def create_new_larpem_banque(self, **kw):
        name = http.request.env.user.name
        default_description = (
            http.request.env["larpem.banque"]
            .default_get(["description"])
            .get("description")
        )
        return http.request.render(
            "larpem.portal_create_larpem_banque",
            {
                "name": name,
                "page_name": "create_larpem_banque",
                "default_description": default_description,
            },
        )

    @http.route(
        "/submitted/larpem_banque",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_larpem_banque(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        if kw.get("description"):
            vals["description"] = kw.get("description")

        new_larpem_banque = request.env["larpem.banque"].sudo().create(vals)
        return werkzeug.utils.redirect(
            f"/my/larpem_banque/{new_larpem_banque.id}"
        )

    @http.route(
        "/new/larpem_banque_compte", type="http", auth="user", website=True
    )
    def create_new_larpem_banque_compte(self, **kw):
        name = http.request.env.user.name
        banque_id = http.request.env["larpem.banque"].search([])
        default_banque_id = (
            http.request.env["larpem.banque.compte"]
            .default_get(["banque_id"])
            .get("banque_id")
        )
        etat_compte = (
            http.request.env["larpem.banque.compte"]
            ._fields["etat_compte"]
            .selection
        )
        default_etat_compte = (
            http.request.env["larpem.banque.compte"]
            .default_get(["etat_compte"])
            .get("etat_compte")
        )
        default_no_compte = (
            http.request.env["larpem.banque.compte"]
            .default_get(["no_compte"])
            .get("no_compte")
        )
        default_nom_personnage = (
            http.request.env["larpem.banque.compte"]
            .default_get(["nom_personnage"])
            .get("nom_personnage")
        )
        personnage_id = http.request.env["larpem.personnage"].search([])
        default_personnage_id = (
            http.request.env["larpem.banque.compte"]
            .default_get(["personnage_id"])
            .get("personnage_id")
        )
        personnage_secondaire_ids = http.request.env[
            "larpem.personnage"
        ].search([])
        lst_default_personnage_secondaire_ids = (
            http.request.env["larpem.banque.compte"]
            .default_get(["personnage_secondaire_ids"])
            .get("personnage_secondaire_ids")
        )
        if lst_default_personnage_secondaire_ids:
            default_personnage_secondaire_ids = (
                lst_default_personnage_secondaire_ids[0][2]
            )
        else:
            default_personnage_secondaire_ids = []
        default_raison_etat_compte = (
            http.request.env["larpem.banque.compte"]
            .default_get(["raison_etat_compte"])
            .get("raison_etat_compte")
        )
        default_total = (
            http.request.env["larpem.banque.compte"]
            .default_get(["total"])
            .get("total")
        )
        type_compte = (
            http.request.env["larpem.banque.compte"]
            ._fields["type_compte"]
            .selection
        )
        default_type_compte = (
            http.request.env["larpem.banque.compte"]
            .default_get(["type_compte"])
            .get("type_compte")
        )
        return http.request.render(
            "larpem.portal_create_larpem_banque_compte",
            {
                "name": name,
                "banque_id": banque_id,
                "etat_compte": etat_compte,
                "personnage_id": personnage_id,
                "personnage_secondaire_ids": personnage_secondaire_ids,
                "type_compte": type_compte,
                "page_name": "create_larpem_banque_compte",
                "default_banque_id": default_banque_id,
                "default_etat_compte": default_etat_compte,
                "default_no_compte": default_no_compte,
                "default_nom_personnage": default_nom_personnage,
                "default_personnage_id": default_personnage_id,
                "default_personnage_secondaire_ids": default_personnage_secondaire_ids,
                "default_raison_etat_compte": default_raison_etat_compte,
                "default_total": default_total,
                "default_type_compte": default_type_compte,
            },
        )

    @http.route(
        "/submitted/larpem_banque_compte",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_larpem_banque_compte(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        if kw.get("banque_id") and kw.get("banque_id").isdigit():
            vals["banque_id"] = int(kw.get("banque_id"))

        if kw.get("etat_compte"):
            vals["etat_compte"] = kw.get("etat_compte")

        if kw.get("no_compte"):
            vals["no_compte"] = kw.get("no_compte")

        if kw.get("nom_personnage"):
            vals["nom_personnage"] = kw.get("nom_personnage")

        if kw.get("personnage_id") and kw.get("personnage_id").isdigit():
            vals["personnage_id"] = int(kw.get("personnage_id"))

        if kw.get("personnage_secondaire_ids"):
            lst_value_personnage_secondaire_ids = [
                (4, int(a))
                for a in request.httprequest.form.getlist(
                    "personnage_secondaire_ids"
                )
            ]
            vals[
                "personnage_secondaire_ids"
            ] = lst_value_personnage_secondaire_ids

        if kw.get("raison_etat_compte"):
            vals["raison_etat_compte"] = kw.get("raison_etat_compte")

        if kw.get("total"):
            total_value = kw.get("total")
            if total_value.replace(".", "", 1).isdigit():
                vals["total"] = float(total_value)

        if kw.get("type_compte"):
            vals["type_compte"] = kw.get("type_compte")

        new_larpem_banque_compte = (
            request.env["larpem.banque.compte"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/larpem_banque_compte/{new_larpem_banque_compte.id}"
        )

    @http.route("/new/larpem_manuel", type="http", auth="user", website=True)
    def create_new_larpem_manuel(self, **kw):
        name = http.request.env.user.name
        default_admin = (
            http.request.env["larpem.manuel"]
            .default_get(["admin"])
            .get("admin")
        )
        default_bullet_description = (
            http.request.env["larpem.manuel"]
            .default_get(["bullet_description"])
            .get("bullet_description")
        )
        default_description = (
            http.request.env["larpem.manuel"]
            .default_get(["description"])
            .get("description")
        )
        default_hide_player = (
            http.request.env["larpem.manuel"]
            .default_get(["hide_player"])
            .get("hide_player")
        )
        default_key = (
            http.request.env["larpem.manuel"].default_get(["key"]).get("key")
        )
        default_model = (
            http.request.env["larpem.manuel"]
            .default_get(["model"])
            .get("model")
        )
        parent_id = http.request.env["larpem.manuel"].search([])
        default_parent_id = (
            http.request.env["larpem.manuel"]
            .default_get(["parent_id"])
            .get("parent_id")
        )
        default_point = (
            http.request.env["larpem.manuel"]
            .default_get(["point"])
            .get("point")
        )
        default_second_bullet_description = (
            http.request.env["larpem.manuel"]
            .default_get(["second_bullet_description"])
            .get("second_bullet_description")
        )
        default_sub_key = (
            http.request.env["larpem.manuel"]
            .default_get(["sub_key"])
            .get("sub_key")
        )
        default_title = (
            http.request.env["larpem.manuel"]
            .default_get(["title"])
            .get("title")
        )
        default_title_html = (
            http.request.env["larpem.manuel"]
            .default_get(["title_html"])
            .get("title_html")
        )
        default_under_level_color = (
            http.request.env["larpem.manuel"]
            .default_get(["under_level_color"])
            .get("under_level_color")
        )
        return http.request.render(
            "larpem.portal_create_larpem_manuel",
            {
                "name": name,
                "parent_id": parent_id,
                "page_name": "create_larpem_manuel",
                "default_admin": default_admin,
                "default_bullet_description": default_bullet_description,
                "default_description": default_description,
                "default_hide_player": default_hide_player,
                "default_key": default_key,
                "default_model": default_model,
                "default_parent_id": default_parent_id,
                "default_point": default_point,
                "default_second_bullet_description": default_second_bullet_description,
                "default_sub_key": default_sub_key,
                "default_title": default_title,
                "default_title_html": default_title_html,
                "default_under_level_color": default_under_level_color,
            },
        )

    @http.route(
        "/submitted/larpem_manuel",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_larpem_manuel(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        default_admin = (
            http.request.env["larpem.manuel"]
            .default_get(["admin"])
            .get("admin")
        )
        if kw.get("admin"):
            vals["admin"] = kw.get("admin") == "True"
        elif default_admin:
            vals["admin"] = False

        if kw.get("bullet_description"):
            vals["bullet_description"] = kw.get("bullet_description")

        if kw.get("description"):
            vals["description"] = kw.get("description")

        default_hide_player = (
            http.request.env["larpem.manuel"]
            .default_get(["hide_player"])
            .get("hide_player")
        )
        if kw.get("hide_player"):
            vals["hide_player"] = kw.get("hide_player") == "True"
        elif default_hide_player:
            vals["hide_player"] = False

        if kw.get("key"):
            vals["key"] = kw.get("key")

        if kw.get("model"):
            vals["model"] = kw.get("model")

        if kw.get("parent_id") and kw.get("parent_id").isdigit():
            vals["parent_id"] = int(kw.get("parent_id"))

        if kw.get("point"):
            vals["point"] = kw.get("point")

        if kw.get("second_bullet_description"):
            vals["second_bullet_description"] = kw.get(
                "second_bullet_description"
            )

        if kw.get("sub_key"):
            vals["sub_key"] = kw.get("sub_key")

        if kw.get("title"):
            vals["title"] = kw.get("title")

        if kw.get("title_html"):
            vals["title_html"] = kw.get("title_html")

        if kw.get("under_level_color"):
            vals["under_level_color"] = kw.get("under_level_color")

        new_larpem_manuel = request.env["larpem.manuel"].sudo().create(vals)
        return werkzeug.utils.redirect(
            f"/my/larpem_manuel/{new_larpem_manuel.id}"
        )

    @http.route(
        "/new/larpem_personnage", type="http", auth="user", website=True
    )
    def create_new_larpem_personnage(self, **kw):
        name = http.request.env.user.name
        default_nom_joueur = (
            http.request.env["larpem.personnage"]
            .default_get(["nom_joueur"])
            .get("nom_joueur")
        )
        partner_id = http.request.env["res.partner"].search(
            [("active", "=", True)]
        )
        default_partner_id = (
            http.request.env["larpem.personnage"]
            .default_get(["partner_id"])
            .get("partner_id")
        )
        return http.request.render(
            "larpem.portal_create_larpem_personnage",
            {
                "name": name,
                "partner_id": partner_id,
                "page_name": "create_larpem_personnage",
                "default_nom_joueur": default_nom_joueur,
                "default_partner_id": default_partner_id,
            },
        )

    @http.route(
        "/submitted/larpem_personnage",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_larpem_personnage(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        if kw.get("nom_joueur"):
            vals["nom_joueur"] = kw.get("nom_joueur")

        if kw.get("partner_id") and kw.get("partner_id").isdigit():
            vals["partner_id"] = int(kw.get("partner_id"))

        new_larpem_personnage = (
            request.env["larpem.personnage"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/larpem_personnage/{new_larpem_personnage.id}"
        )

    @http.route(
        "/new/larpem_system_point", type="http", auth="user", website=True
    )
    def create_new_larpem_system_point(self, **kw):
        name = http.request.env.user.name
        default_explication = (
            http.request.env["larpem.system_point"]
            .default_get(["explication"])
            .get("explication")
        )
        default_formule = (
            http.request.env["larpem.system_point"]
            .default_get(["formule"])
            .get("formule")
        )
        default_hide_value = (
            http.request.env["larpem.system_point"]
            .default_get(["hide_value"])
            .get("hide_value")
        )
        default_identifiant = (
            http.request.env["larpem.system_point"]
            .default_get(["identifiant"])
            .get("identifiant")
        )
        default_init_value = (
            http.request.env["larpem.system_point"]
            .default_get(["init_value"])
            .get("init_value")
        )
        default_invisible = (
            http.request.env["larpem.system_point"]
            .default_get(["invisible"])
            .get("invisible")
        )
        default_max_value = (
            http.request.env["larpem.system_point"]
            .default_get(["max_value"])
            .get("max_value")
        )
        default_min_value = (
            http.request.env["larpem.system_point"]
            .default_get(["min_value"])
            .get("min_value")
        )
        default_required_value = (
            http.request.env["larpem.system_point"]
            .default_get(["required_value"])
            .get("required_value")
        )
        type = (
            http.request.env["larpem.system_point"]._fields["type"].selection
        )
        default_type = (
            http.request.env["larpem.system_point"]
            .default_get(["type"])
            .get("type")
        )
        return http.request.render(
            "larpem.portal_create_larpem_system_point",
            {
                "name": name,
                "type": type,
                "page_name": "create_larpem_system_point",
                "default_explication": default_explication,
                "default_formule": default_formule,
                "default_hide_value": default_hide_value,
                "default_identifiant": default_identifiant,
                "default_init_value": default_init_value,
                "default_invisible": default_invisible,
                "default_max_value": default_max_value,
                "default_min_value": default_min_value,
                "default_required_value": default_required_value,
                "default_type": default_type,
            },
        )

    @http.route(
        "/submitted/larpem_system_point",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_larpem_system_point(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        if kw.get("explication"):
            vals["explication"] = kw.get("explication")

        if kw.get("formule"):
            vals["formule"] = kw.get("formule")

        default_hide_value = (
            http.request.env["larpem.system_point"]
            .default_get(["hide_value"])
            .get("hide_value")
        )
        if kw.get("hide_value"):
            vals["hide_value"] = kw.get("hide_value") == "True"
        elif default_hide_value:
            vals["hide_value"] = False

        if kw.get("identifiant"):
            vals["identifiant"] = kw.get("identifiant")

        if kw.get("init_value"):
            init_value_value = kw.get("init_value")
            if init_value_value.isdigit():
                vals["init_value"] = int(init_value_value)

        default_invisible = (
            http.request.env["larpem.system_point"]
            .default_get(["invisible"])
            .get("invisible")
        )
        if kw.get("invisible"):
            vals["invisible"] = kw.get("invisible") == "True"
        elif default_invisible:
            vals["invisible"] = False

        if kw.get("max_value"):
            max_value_value = kw.get("max_value")
            if max_value_value.isdigit():
                vals["max_value"] = int(max_value_value)

        if kw.get("min_value"):
            min_value_value = kw.get("min_value")
            if min_value_value.isdigit():
                vals["min_value"] = int(min_value_value)

        default_required_value = (
            http.request.env["larpem.system_point"]
            .default_get(["required_value"])
            .get("required_value")
        )
        if kw.get("required_value"):
            vals["required_value"] = kw.get("required_value") == "True"
        elif default_required_value:
            vals["required_value"] = False

        if kw.get("type"):
            vals["type"] = kw.get("type")

        new_larpem_system_point = (
            request.env["larpem.system_point"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/larpem_system_point/{new_larpem_system_point.id}"
        )

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
