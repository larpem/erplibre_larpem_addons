import logging
import os
import time

from .pylib.doc_generator import doc_generator_gspread

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "larpem"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        path_client_secret = os.path.join(os.path.dirname(__file__), "client_secret.json")
        file_url = ""

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        categ_id = env["ir.module.category"].search(
            [("name", "=", "Uncategorized")]
        )
        value = {
            "shortdesc": short_name,
            "name": MODULE_NAME,
            "license": "AGPL-3",
            "category_id": categ_id.id,
            "summary": "",
            "author": "TechnoLibre",
            "website": "",
            "application": True,
            "enable_sync_code": True,
            "path_sync_code": path_module_generate,
            # "icon": os.path.join(
            #     os.path.basename(os.path.dirname(os.path.dirname(__file__))),
            #     "static",
            #     "description",
            #     "code_generator_icon.png",
            # ),
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_sync_template"] = False
        value["ignore_fields"] = ""
        value["post_init_hook_show"] = False
        value["uninstall_hook_show"] = False
        value["post_init_hook_feature_code_generator"] = False
        value["uninstall_hook_feature_code_generator"] = False

        value["hook_constant_code"] = f'MODULE_NAME = "{MODULE_NAME}"'

        code_generator_id = env["code.generator.module"].create(value)

        # Modification of field before migration

        before_time = time.process_time()

        doc_gspread = doc_generator_gspread.DocGeneratorGSpread(path_client_secret, file_url)
        doc_generator = doc_gspread.get_instance()
        if not doc_generator:
            raise Exception("Cannot read google spread credentials. Did you have client_secret.json and good url?")

        status = doc_generator.generate_doc()
        if not status:
            error = doc_generator.get_error(force_error=True)
            raise Exception(f"Error from generate_doc : {error}")

        document = doc_generator.get_generated_doc()

        # System point
        model_model = "larpem.system_point"
        model_name = "Système point"
        dct_model = {
            "description": "Système de pointage de LARPEM",
        }
        dct_field = {
            "description": {
                "field_description": "description",
                "ttype": "char",
            },
            "explication": {
                "field_description": "Explication",
                "ttype": "char",
            },
            "type": {
                "field_description": "Type",
                "ttype": "char",
            },
            "name": {
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_aliment = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        lst_system_point = document.get("system_point")

        # keys = list(lst_system_point[0].keys())

        after_time = time.process_time()
        _logger.info(
            "DEBUG time execution hook update model db before generate_module"
            f" {after_time - before_time}"
        )

        # Generate view
        # Action generate view
        wizard_view = env["code.generator.generate.views.wizard"].create(
            {
                "code_generator_id": code_generator_id.id,
                "enable_generate_all": True,
            }
        )

        wizard_view.button_generate_views()

        # Generate module
        value = {"code_generator_ids": code_generator_id.ids}
        env["code.generator.writer"].create(value)


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        code_generator_id = env["code.generator.module"].search(
            [("name", "=", MODULE_NAME)]
        )
        if code_generator_id:
            code_generator_id.unlink()
