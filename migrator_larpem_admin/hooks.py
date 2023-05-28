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

        # manuel
        lst_manuel = document.get("manual")
        for dct_manuel in lst_manuel:
            add_manuel_section(env, dct_manuel)

        _logger.info("Import data from user database")
        # Import user data
        with open(path_db_json, "r") as f:
            data = json.load(f)
        db_user = data.get("_default")
        for bd_id, dct_user in db_user.items():
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
            lst_char = dct_user.get("character")
            if len(lst_char) < 1:
                _logger.warning(
                    f"User name {name} id {bd_id} missing character"
                )
            elif len(lst_char) > 1:
                _logger.warning(
                    f"User name {name} id {bd_id} has multiple character, why?"
                )
            else:
                char = lst_char[0]
                char_value = {
                    "name": char.get("name", False),
                    "partner_id": partner_id.id,
                }

                env["larpem.personnage"].create(char_value)

            zip_str = dct_user.get("postal_code")
            if zip_str:
                partner_id.zip = zip_str

        after_time = time.process_time()
        _logger.info(
            "DEBUG time execution hook update model db before generate_module"
            f" {after_time - before_time}"
        )


def add_manuel_section(env, dct_manuel, parent_id=None):
    dct_value = {}
    if "title" in dct_manuel.keys():
        dct_value["title"] = dct_manuel.get("title")
    if "title_html" in dct_manuel.keys():
        dct_value["title_html"] = dct_manuel.get("title_html")
    if "sub_key" in dct_manuel.keys():
        dct_value["sub_key"] = dct_manuel.get("sub_key")
    if "model" in dct_manuel.keys():
        dct_value["model"] = dct_manuel.get("model")
    if "admin" in dct_manuel.keys():
        dct_value["admin"] = dct_manuel.get("admin")
    if "hide_player" in dct_manuel.keys():
        dct_value["hide_player"] = dct_manuel.get("hide_player")
    if "point" in dct_manuel.keys():
        # TODO need to change
        dct_value["point"] = dct_manuel.get("point")
    if "description" in dct_manuel.keys():
        # TODO check double list, it's a bullet point
        dct_value["description"] = (
            str(dct_manuel.get("description"))
            .replace("['", "")
            .replace("']", "\n")
            .replace("[", "")
            .replace("]", "\n")
        )
        # try:
        #     dct_value["description"] = "\n".join(dct_manuel.get("description"))
        # except Exception as e:
        #     # Suppose double list
        #     try:
        #         dct_value["description"] = "\n".join(["\n".join(a) if type(a) is list else a for a in dct_manuel.get("description")])
        #     except Exception as e:
        #         print(e)
    if parent_id:
        dct_value["parent_id"] = parent_id.id

    manuel_id = env["larpem.manuel"].create(dct_value)
    if "section" in dct_manuel.keys():
        for section in dct_manuel.get("section"):
            add_manuel_section(env, section, parent_id=manuel_id)


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # code_generator_id = env["code.generator.module"].search(
        #     [("name", "=", MODULE_NAME)]
        # )
        # if code_generator_id:
        #     code_generator_id.unlink()
