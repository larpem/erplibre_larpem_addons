import json
import logging
import os
import time

from odoo import SUPERUSER_ID, _, api, fields, models

from .pylib.doc_generator import doc_generator_gspread

_logger = logging.getLogger(__name__)

MODULE_NAME = "larpem"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        path_client_secret = os.path.join(
            os.path.dirname(__file__), "client_secret.json"
        )
        file_url = ""
        path_db_json = os.path.join(os.path.dirname(__file__), "tl_user.json")
        if not os.path.isfile(path_client_secret):
            raise Exception(f"Missing file {path_client_secret}")
        if not os.path.isfile(path_db_json):
            raise Exception(f"Missing file {path_db_json}")

        before_time = time.process_time()

        doc_gspread = doc_generator_gspread.DocGeneratorGSpread(
            path_client_secret, file_url
        )
        doc_generator = doc_gspread.get_instance()
        if not doc_generator:
            raise Exception(
                "Cannot read google spread credentials. Did you have"
                " client_secret.json and good url?"
            )

        status = doc_generator.generate_doc()
        if not status:
            error = doc_generator.get_error(force_error=True)
            raise Exception(f"Error from generate_doc : {error}")

        document = doc_generator.get_generated_doc()

        # System point
        lst_system_point = document.get("system_point")
        for sp in lst_system_point:
            if "description" in sp.keys():
                sp["identifiant"] = sp.pop("name")
                sp["name"] = sp.pop("description")
            if "required" in sp.keys():
                sp["required_value"] = sp.pop("required")
            if "initial" in sp.keys():
                sp["init_value"] = sp.pop("initial")
            if "min" in sp.keys():
                sp["min_value"] = sp.pop("min")
            if "max" in sp.keys():
                sp["max_value"] = sp.pop("max")

        env["larpem.system_point"].create(lst_system_point)

        # manual
        lst_manual = document.get("manual")
        for dct_manual in lst_manual:
            add_manual_section(env, dct_manual)

        _logger.info("Import data from user database")
        # Import user data
        with open(path_db_json, "r") as f:
            data = json.load(f)
        db_user = data.get("_default")
        for dct_user in db_user.values():
            name = dct_user.get("name")
            email = dct_user.get("email")
            if email:
                # _logger.warning(f"Missing email for user {name}. Ignore it")
                # continue
                user_id = env["res.users"].create(
                    {
                        "name": name,
                        "login": email,
                        "email": email,
                        "groups_id": [
                            (6, 0, [env.ref("base.group_portal").id])
                        ],
                    }
                )
                partner_id = user_id.partner_id
            else:
                # Don't create user, only the contact information
                partner_id = env["res.partner"].create(
                    {
                        "name": name,
                    }
                )
            zip_str = dct_user.get("postal_code")
            if zip_str:
                partner_id.zip = zip_str

        after_time = time.process_time()
        _logger.info(
            "DEBUG time execution hook update model db before generate_module"
            f" {after_time - before_time}"
        )


def add_manual_section(env, dct_manual, parent_id=None):
    dct_value = {}
    if "title" in dct_manual.keys():
        dct_value["title"] = dct_manual.get("title")
    if "title_html" in dct_manual.keys():
        dct_value["title_html"] = dct_manual.get("title_html")
    if "sub_key" in dct_manual.keys():
        dct_value["sub_key"] = dct_manual.get("sub_key")
    if "model" in dct_manual.keys():
        dct_value["model"] = dct_manual.get("model")
    if "admin" in dct_manual.keys():
        dct_value["admin"] = dct_manual.get("admin")
    if "hide_player" in dct_manual.keys():
        dct_value["hide_player"] = dct_manual.get("hide_player")
    if "point" in dct_manual.keys():
        # TODO need to change
        dct_value["point"] = dct_manual.get("point")
    if "description" in dct_manual.keys():
        # TODO check double list, it's a bullet point
        dct_value["description"] = (
            str(dct_manual.get("description"))
            .replace("['", "")
            .replace("']", "\n")
            .replace("[", "")
            .replace("]", "\n")
        )
        # try:
        #     dct_value["description"] = "\n".join(dct_manual.get("description"))
        # except Exception as e:
        #     # Suppose double list
        #     try:
        #         dct_value["description"] = "\n".join(["\n".join(a) if type(a) is list else a for a in dct_manual.get("description")])
        #     except Exception as e:
        #         print(e)
    if parent_id:
        dct_value["parent_id"] = parent_id.id

    manual_id = env["larpem.manual"].create(dct_value)
    if "section" in dct_manual.keys():
        for section in dct_manual.get("section"):
            add_manual_section(env, section, parent_id=manual_id)


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # code_generator_id = env["code.generator.module"].search(
        #     [("name", "=", MODULE_NAME)]
        # )
        # if code_generator_id:
        #     code_generator_id.unlink()
