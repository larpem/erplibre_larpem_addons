from collections import OrderedDict
from operator import itemgetter

from odoo import _, http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem


class LarpemController(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(LarpemController, self)._prepare_portal_layout_values()
        # values["larpem_banque_count"] = request.env[
        #     "larpem.banque"
        # ].search_count([])
        # values["larpem_banque_compte_count"] = request.env[
        #     "larpem.banque.compte"
        # ].search_count([])
        # values["larpem_manuel_count"] = request.env[
        #     "larpem.manuel"
        # ].search_count([])
        partner_id = http.request.env.user.partner_id
        larpem_personnage_id = (
            http.request.env["larpem.personnage"]
            .sudo()
            .search([("partner_id", "=", partner_id.id)], limit=1)
        )
        values["larpem_personnage_count"] = request.env[
            "larpem.personnage"
        ].search_count([("id", "=", larpem_personnage_id.id)])
        # values["larpem_system_point_count"] = request.env[
        #     "larpem.system_point"
        # ].search_count([])
        return values

    # ------------------------------------------------------------
    # My Larpem Banque
    # ------------------------------------------------------------
    # def _larpem_banque_get_page_view_values(
    #     self, larpem_banque, access_token, **kwargs
    # ):
    #     values = {
    #         "page_name": "larpem_banque",
    #         "larpem_banque": larpem_banque,
    #         "user": request.env.user,
    #     }
    #     return self._get_page_view_values(
    #         larpem_banque,
    #         access_token,
    #         values,
    #         "my_larpem_banques_history",
    #         False,
    #         **kwargs,
    #     )
    #
    # @http.route(
    #     ["/my/larpem_banques", "/my/larpem_banques/page/<int:page>"],
    #     type="http",
    #     auth="user",
    #     website=True,
    # )
    # def portal_my_larpem_banques(
    #     self,
    #     page=1,
    #     date_begin=None,
    #     date_end=None,
    #     sortby=None,
    #     filterby=None,
    #     search=None,
    #     search_in="content",
    #     **kw,
    # ):
    #     values = self._prepare_portal_layout_values()
    #     LarpemBanque = request.env["larpem.banque"]
    #     domain = []
    #
    #     searchbar_sortings = {
    #         "date": {"label": _("Newest"), "order": "create_date desc"},
    #         "name": {"label": _("Name"), "order": "name"},
    #     }
    #     searchbar_filters = {
    #         "all": {"label": _("All"), "domain": []},
    #     }
    #     searchbar_inputs = {}
    #     searchbar_groupby = {}
    #
    #     # default sort by value
    #     if not sortby:
    #         sortby = "date"
    #     order = searchbar_sortings[sortby]["order"]
    #     # default filter by value
    #     if not filterby:
    #         filterby = "all"
    #     domain = searchbar_filters[filterby]["domain"]
    #
    #     # search
    #     if search and search_in:
    #         search_domain = []
    #         domain += search_domain
    #     # archive groups - Default Group By 'create_date'
    #     archive_groups = self._get_archive_groups("larpem.banque", domain)
    #     if date_begin and date_end:
    #         domain += [
    #             ("create_date", ">", date_begin),
    #             ("create_date", "<=", date_end),
    #         ]
    #     # larpem_banques count
    #     larpem_banque_count = LarpemBanque.search_count(domain)
    #     # pager
    #     pager = portal_pager(
    #         url="/my/larpem_banques",
    #         url_args={
    #             "date_begin": date_begin,
    #             "date_end": date_end,
    #             "sortby": sortby,
    #             "filterby": filterby,
    #             "search_in": search_in,
    #             "search": search,
    #         },
    #         total=larpem_banque_count,
    #         page=page,
    #         step=self._items_per_page,
    #     )
    #
    #     # content according to pager and archive selected
    #     larpem_banques = LarpemBanque.search(
    #         domain,
    #         order=order,
    #         limit=self._items_per_page,
    #         offset=pager["offset"],
    #     )
    #     request.session["my_larpem_banques_history"] = larpem_banques.ids[:100]
    #
    #     values.update(
    #         {
    #             "date": date_begin,
    #             "date_end": date_end,
    #             "larpem_banques": larpem_banques,
    #             "page_name": "larpem_banque",
    #             "archive_groups": archive_groups,
    #             "default_url": "/my/larpem_banques",
    #             "pager": pager,
    #             "searchbar_sortings": searchbar_sortings,
    #             "searchbar_groupby": searchbar_groupby,
    #             "searchbar_inputs": searchbar_inputs,
    #             "search_in": search_in,
    #             "searchbar_filters": OrderedDict(
    #                 sorted(searchbar_filters.items())
    #             ),
    #             "sortby": sortby,
    #             "filterby": filterby,
    #         }
    #     )
    #     return request.render("larpem.portal_my_larpem_banques", values)
    #
    # @http.route(
    #     ["/my/larpem_banque/<int:larpem_banque_id>"],
    #     type="http",
    #     auth="public",
    #     website=True,
    # )
    # def portal_my_larpem_banque(
    #     self, larpem_banque_id=None, access_token=None, **kw
    # ):
    #     try:
    #         larpem_banque_sudo = self._document_check_access(
    #             "larpem.banque", larpem_banque_id, access_token
    #         )
    #     except (AccessError, MissingError):
    #         return request.redirect("/my")
    #
    #     values = self._larpem_banque_get_page_view_values(
    #         larpem_banque_sudo, access_token, **kw
    #     )
    #     return request.render("larpem.portal_my_larpem_banque", values)
    #
    # # ------------------------------------------------------------
    # # My Larpem Banque Compte
    # # ------------------------------------------------------------
    # def _larpem_banque_compte_get_page_view_values(
    #     self, larpem_banque_compte, access_token, **kwargs
    # ):
    #     values = {
    #         "page_name": "larpem_banque_compte",
    #         "larpem_banque_compte": larpem_banque_compte,
    #         "user": request.env.user,
    #     }
    #     return self._get_page_view_values(
    #         larpem_banque_compte,
    #         access_token,
    #         values,
    #         "my_larpem_banque_comptes_history",
    #         False,
    #         **kwargs,
    #     )
    #
    # @http.route(
    #     [
    #         "/my/larpem_banque_comptes",
    #         "/my/larpem_banque_comptes/page/<int:page>",
    #     ],
    #     type="http",
    #     auth="user",
    #     website=True,
    # )
    # def portal_my_larpem_banque_comptes(
    #     self,
    #     page=1,
    #     date_begin=None,
    #     date_end=None,
    #     sortby=None,
    #     filterby=None,
    #     search=None,
    #     search_in="content",
    #     **kw,
    # ):
    #     values = self._prepare_portal_layout_values()
    #     LarpemBanqueCompte = request.env["larpem.banque.compte"]
    #     domain = []
    #
    #     searchbar_sortings = {
    #         "date": {"label": _("Newest"), "order": "create_date desc"},
    #         "name": {"label": _("Name"), "order": "name"},
    #     }
    #     searchbar_filters = {
    #         "all": {"label": _("All"), "domain": []},
    #     }
    #     searchbar_inputs = {}
    #     searchbar_groupby = {}
    #
    #     # default sort by value
    #     if not sortby:
    #         sortby = "date"
    #     order = searchbar_sortings[sortby]["order"]
    #     # default filter by value
    #     if not filterby:
    #         filterby = "all"
    #     domain = searchbar_filters[filterby]["domain"]
    #
    #     # search
    #     if search and search_in:
    #         search_domain = []
    #         domain += search_domain
    #     # archive groups - Default Group By 'create_date'
    #     archive_groups = self._get_archive_groups(
    #         "larpem.banque.compte", domain
    #     )
    #     if date_begin and date_end:
    #         domain += [
    #             ("create_date", ">", date_begin),
    #             ("create_date", "<=", date_end),
    #         ]
    #     # larpem_banque_comptes count
    #     larpem_banque_compte_count = LarpemBanqueCompte.search_count(domain)
    #     # pager
    #     pager = portal_pager(
    #         url="/my/larpem_banque_comptes",
    #         url_args={
    #             "date_begin": date_begin,
    #             "date_end": date_end,
    #             "sortby": sortby,
    #             "filterby": filterby,
    #             "search_in": search_in,
    #             "search": search,
    #         },
    #         total=larpem_banque_compte_count,
    #         page=page,
    #         step=self._items_per_page,
    #     )
    #
    #     # content according to pager and archive selected
    #     larpem_banque_comptes = LarpemBanqueCompte.search(
    #         domain,
    #         order=order,
    #         limit=self._items_per_page,
    #         offset=pager["offset"],
    #     )
    #     request.session[
    #         "my_larpem_banque_comptes_history"
    #     ] = larpem_banque_comptes.ids[:100]
    #
    #     values.update(
    #         {
    #             "date": date_begin,
    #             "date_end": date_end,
    #             "larpem_banque_comptes": larpem_banque_comptes,
    #             "page_name": "larpem_banque_compte",
    #             "archive_groups": archive_groups,
    #             "default_url": "/my/larpem_banque_comptes",
    #             "pager": pager,
    #             "searchbar_sortings": searchbar_sortings,
    #             "searchbar_groupby": searchbar_groupby,
    #             "searchbar_inputs": searchbar_inputs,
    #             "search_in": search_in,
    #             "searchbar_filters": OrderedDict(
    #                 sorted(searchbar_filters.items())
    #             ),
    #             "sortby": sortby,
    #             "filterby": filterby,
    #         }
    #     )
    #     return request.render("larpem.portal_my_larpem_banque_comptes", values)
    #
    # @http.route(
    #     ["/my/larpem_banque_compte/<int:larpem_banque_compte_id>"],
    #     type="http",
    #     auth="public",
    #     website=True,
    # )
    # def portal_my_larpem_banque_compte(
    #     self, larpem_banque_compte_id=None, access_token=None, **kw
    # ):
    #     try:
    #         larpem_banque_compte_sudo = self._document_check_access(
    #             "larpem.banque.compte", larpem_banque_compte_id, access_token
    #         )
    #     except (AccessError, MissingError):
    #         return request.redirect("/my")
    #
    #     values = self._larpem_banque_compte_get_page_view_values(
    #         larpem_banque_compte_sudo, access_token, **kw
    #     )
    #     return request.render("larpem.portal_my_larpem_banque_compte", values)
    #
    # # ------------------------------------------------------------
    # # My Larpem Manuel
    # # ------------------------------------------------------------
    # def _larpem_manuel_get_page_view_values(
    #     self, larpem_manuel, access_token, **kwargs
    # ):
    #     values = {
    #         "page_name": "larpem_manuel",
    #         "larpem_manuel": larpem_manuel,
    #         "user": request.env.user,
    #     }
    #     return self._get_page_view_values(
    #         larpem_manuel,
    #         access_token,
    #         values,
    #         "my_larpem_manuels_history",
    #         False,
    #         **kwargs,
    #     )
    #
    # @http.route(
    #     ["/my/larpem_manuels", "/my/larpem_manuels/page/<int:page>"],
    #     type="http",
    #     auth="user",
    #     website=True,
    # )
    # def portal_my_larpem_manuels(
    #     self,
    #     page=1,
    #     date_begin=None,
    #     date_end=None,
    #     sortby=None,
    #     filterby=None,
    #     search=None,
    #     search_in="content",
    #     **kw,
    # ):
    #     values = self._prepare_portal_layout_values()
    #     LarpemManuel = request.env["larpem.manuel"]
    #     domain = []
    #
    #     searchbar_sortings = {
    #         "date": {"label": _("Newest"), "order": "create_date desc"},
    #         "name": {"label": _("Name"), "order": "name"},
    #     }
    #     searchbar_filters = {
    #         "all": {"label": _("All"), "domain": []},
    #     }
    #     searchbar_inputs = {}
    #     searchbar_groupby = {}
    #
    #     # default sort by value
    #     if not sortby:
    #         sortby = "date"
    #     order = searchbar_sortings[sortby]["order"]
    #     # default filter by value
    #     if not filterby:
    #         filterby = "all"
    #     domain = searchbar_filters[filterby]["domain"]
    #
    #     # search
    #     if search and search_in:
    #         search_domain = []
    #         domain += search_domain
    #     # archive groups - Default Group By 'create_date'
    #     archive_groups = self._get_archive_groups("larpem.manuel", domain)
    #     if date_begin and date_end:
    #         domain += [
    #             ("create_date", ">", date_begin),
    #             ("create_date", "<=", date_end),
    #         ]
    #     # larpem_manuels count
    #     larpem_manuel_count = LarpemManuel.search_count(domain)
    #     # pager
    #     pager = portal_pager(
    #         url="/my/larpem_manuels",
    #         url_args={
    #             "date_begin": date_begin,
    #             "date_end": date_end,
    #             "sortby": sortby,
    #             "filterby": filterby,
    #             "search_in": search_in,
    #             "search": search,
    #         },
    #         total=larpem_manuel_count,
    #         page=page,
    #         step=self._items_per_page,
    #     )
    #
    #     # content according to pager and archive selected
    #     larpem_manuels = LarpemManuel.search(
    #         domain,
    #         order=order,
    #         limit=self._items_per_page,
    #         offset=pager["offset"],
    #     )
    #     request.session["my_larpem_manuels_history"] = larpem_manuels.ids[:100]
    #
    #     values.update(
    #         {
    #             "date": date_begin,
    #             "date_end": date_end,
    #             "larpem_manuels": larpem_manuels,
    #             "page_name": "larpem_manuel",
    #             "archive_groups": archive_groups,
    #             "default_url": "/my/larpem_manuels",
    #             "pager": pager,
    #             "searchbar_sortings": searchbar_sortings,
    #             "searchbar_groupby": searchbar_groupby,
    #             "searchbar_inputs": searchbar_inputs,
    #             "search_in": search_in,
    #             "searchbar_filters": OrderedDict(
    #                 sorted(searchbar_filters.items())
    #             ),
    #             "sortby": sortby,
    #             "filterby": filterby,
    #         }
    #     )
    #     return request.render("larpem.portal_my_larpem_manuels", values)
    #
    # @http.route(
    #     ["/my/larpem_manuel/<int:larpem_manuel_id>"],
    #     type="http",
    #     auth="public",
    #     website=True,
    # )
    # def portal_my_larpem_manuel(
    #     self, larpem_manuel_id=None, access_token=None, **kw
    # ):
    #     try:
    #         larpem_manuel_sudo = self._document_check_access(
    #             "larpem.manuel", larpem_manuel_id, access_token
    #         )
    #     except (AccessError, MissingError):
    #         return request.redirect("/my")
    #
    #     values = self._larpem_manuel_get_page_view_values(
    #         larpem_manuel_sudo, access_token, **kw
    #     )
    #     return request.render("larpem.portal_my_larpem_manuel", values)

    # ------------------------------------------------------------
    # My Larpem Personnage
    # ------------------------------------------------------------
    def _larpem_personnage_get_page_view_values(
        self, larpem_personnage, access_token, **kwargs
    ):
        values = {
            "page_name": "larpem_personnage",
            "larpem_personnage": larpem_personnage,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            larpem_personnage,
            access_token,
            values,
            "my_larpem_personnages_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/larpem_personnages", "/my/larpem_personnages/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_larpem_personnages(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        LarpemPersonnage = request.env["larpem.personnage"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain

        partner_id = http.request.env.user.partner_id
        larpem_personnage_id = (
            http.request.env["larpem.personnage"]
            .sudo()
            .search([("partner_id", "=", partner_id.id)], limit=1)
        )
        domain += [("id", "=", larpem_personnage_id.id)]
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("larpem.personnage", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # larpem_personnages count
        larpem_personnage_count = LarpemPersonnage.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/larpem_personnages",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=larpem_personnage_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        larpem_personnages = LarpemPersonnage.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_larpem_personnages_history"
        ] = larpem_personnages.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "larpem_personnages": larpem_personnages,
                "page_name": "larpem_personnage",
                "archive_groups": archive_groups,
                "default_url": "/my/larpem_personnages",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render("larpem.portal_my_larpem_personnages", values)

    @http.route(
        ["/my/larpem_personnage/<int:larpem_personnage_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_larpem_personnage(
        self, larpem_personnage_id=None, access_token=None, **kw
    ):
        try:
            larpem_personnage_sudo = self._document_check_access(
                "larpem.personnage", larpem_personnage_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        partner_id = http.request.env.user.partner_id
        personnage_id = (
            http.request.env["larpem.personnage"]
            .sudo()
            .search([("partner_id", "=", partner_id.id)], limit=1)
        )
        if larpem_personnage_id != personnage_id.id:
            return request.redirect("/my")

        values = self._larpem_personnage_get_page_view_values(
            larpem_personnage_sudo, access_token, **kw
        )
        return request.render("larpem.portal_my_larpem_personnage", values)

    # ------------------------------------------------------------
    # My Larpem System_Point
    # ------------------------------------------------------------
    # def _larpem_system_point_get_page_view_values(
    #     self, larpem_system_point, access_token, **kwargs
    # ):
    #     values = {
    #         "page_name": "larpem_system_point",
    #         "larpem_system_point": larpem_system_point,
    #         "user": request.env.user,
    #     }
    #     return self._get_page_view_values(
    #         larpem_system_point,
    #         access_token,
    #         values,
    #         "my_larpem_system_points_history",
    #         False,
    #         **kwargs,
    #     )
    #
    # @http.route(
    #     [
    #         "/my/larpem_system_points",
    #         "/my/larpem_system_points/page/<int:page>",
    #     ],
    #     type="http",
    #     auth="user",
    #     website=True,
    # )
    # def portal_my_larpem_system_points(
    #     self,
    #     page=1,
    #     date_begin=None,
    #     date_end=None,
    #     sortby=None,
    #     filterby=None,
    #     search=None,
    #     search_in="content",
    #     **kw,
    # ):
    #     values = self._prepare_portal_layout_values()
    #     LarpemSystemPoint = request.env["larpem.system_point"]
    #     domain = []
    #
    #     searchbar_sortings = {
    #         "date": {"label": _("Newest"), "order": "create_date desc"},
    #         "name": {"label": _("Name"), "order": "name"},
    #     }
    #     searchbar_filters = {
    #         "all": {"label": _("All"), "domain": []},
    #     }
    #     searchbar_inputs = {}
    #     searchbar_groupby = {}
    #
    #     # default sort by value
    #     if not sortby:
    #         sortby = "date"
    #     order = searchbar_sortings[sortby]["order"]
    #     # default filter by value
    #     if not filterby:
    #         filterby = "all"
    #     domain = searchbar_filters[filterby]["domain"]
    #
    #     # search
    #     if search and search_in:
    #         search_domain = []
    #         domain += search_domain
    #     # archive groups - Default Group By 'create_date'
    #     archive_groups = self._get_archive_groups(
    #         "larpem.system_point", domain
    #     )
    #     if date_begin and date_end:
    #         domain += [
    #             ("create_date", ">", date_begin),
    #             ("create_date", "<=", date_end),
    #         ]
    #     # larpem_system_points count
    #     larpem_system_point_count = LarpemSystemPoint.search_count(domain)
    #     # pager
    #     pager = portal_pager(
    #         url="/my/larpem_system_points",
    #         url_args={
    #             "date_begin": date_begin,
    #             "date_end": date_end,
    #             "sortby": sortby,
    #             "filterby": filterby,
    #             "search_in": search_in,
    #             "search": search,
    #         },
    #         total=larpem_system_point_count,
    #         page=page,
    #         step=self._items_per_page,
    #     )
    #
    #     # content according to pager and archive selected
    #     larpem_system_points = LarpemSystemPoint.search(
    #         domain,
    #         order=order,
    #         limit=self._items_per_page,
    #         offset=pager["offset"],
    #     )
    #     request.session[
    #         "my_larpem_system_points_history"
    #     ] = larpem_system_points.ids[:100]
    #
    #     values.update(
    #         {
    #             "date": date_begin,
    #             "date_end": date_end,
    #             "larpem_system_points": larpem_system_points,
    #             "page_name": "larpem_system_point",
    #             "archive_groups": archive_groups,
    #             "default_url": "/my/larpem_system_points",
    #             "pager": pager,
    #             "searchbar_sortings": searchbar_sortings,
    #             "searchbar_groupby": searchbar_groupby,
    #             "searchbar_inputs": searchbar_inputs,
    #             "search_in": search_in,
    #             "searchbar_filters": OrderedDict(
    #                 sorted(searchbar_filters.items())
    #             ),
    #             "sortby": sortby,
    #             "filterby": filterby,
    #         }
    #     )
    #     return request.render("larpem.portal_my_larpem_system_points", values)
    #
    # @http.route(
    #     ["/my/larpem_system_point/<int:larpem_system_point_id>"],
    #     type="http",
    #     auth="public",
    #     website=True,
    # )
    # def portal_my_larpem_system_point(
    #     self, larpem_system_point_id=None, access_token=None, **kw
    # ):
    #     try:
    #         larpem_system_point_sudo = self._document_check_access(
    #             "larpem.system_point", larpem_system_point_id, access_token
    #         )
    #     except (AccessError, MissingError):
    #         return request.redirect("/my")
    #
    #     values = self._larpem_system_point_get_page_view_values(
    #         larpem_system_point_sudo, access_token, **kw
    #     )
    #     return request.render("larpem.portal_my_larpem_system_point", values)
