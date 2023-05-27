import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "larpem"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = "addons/larpem_erplibre_larpem_addons"

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        categ_id = env["ir.module.category"].search(
            [("name", "=", "Uncategorized")], limit=1
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
            "icon": os.path.join(
                os.path.dirname(__file__),
                "static",
                "description",
                "code_generator_icon.png",
            ),
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_sync_template"] = True
        value["ignore_fields"] = ""
        value["post_init_hook_show"] = False
        value["uninstall_hook_show"] = False
        value["post_init_hook_feature_code_generator"] = False
        value["uninstall_hook_feature_code_generator"] = False

        value["hook_constant_code"] = f'MODULE_NAME = "{MODULE_NAME}"'

        code_generator_id = env["code.generator.module"].create(value)

        # Add/Update Larpem System Point
        model_model = "larpem.system_point"
        model_name = "larpem_system_point"
        dct_model = {
            "description": "Système de pointage de LARPEM",
        }
        dct_field = {
            "explication": {
                "code_generator_sequence": 4,
                "field_description": "Explication",
                "ttype": "char",
            },
            "formule": {
                "code_generator_sequence": 8,
                "field_description": "Formule",
                "ttype": "char",
            },
            "hide_value": {
                "code_generator_sequence": 9,
                "field_description": "Cache la valeur",
                "help": "TODO à définir",
                "ttype": "boolean",
            },
            "identifiant": {
                "code_generator_sequence": 3,
                "field_description": "Identifiant",
                "ttype": "char",
            },
            "init_value": {
                "code_generator_sequence": 5,
                "field_description": "Valeur initiale",
                "ttype": "integer",
            },
            "invisible": {
                "code_generator_sequence": 11,
                "field_description": "Invisible",
                "help": "TODO à définir",
                "ttype": "boolean",
            },
            "max_value": {
                "code_generator_sequence": 7,
                "field_description": "Valeur maximal",
                "ttype": "integer",
            },
            "min_value": {
                "code_generator_sequence": 6,
                "field_description": "Valeur minimal",
                "ttype": "integer",
            },
            "name": {
                "code_generator_sequence": 2,
                "field_description": "Description",
                "ttype": "char",
            },
            "required_value": {
                "code_generator_sequence": 10,
                "field_description": "Valeur requise",
                "ttype": "boolean",
            },
            "type": {
                "code_generator_sequence": 12,
                "default": "ressource",
                "field_description": "Type",
                "required": True,
                "selection": (
                    "[('attribut', 'Attribut'), ('ressource', 'Ressource')]"
                ),
                "ttype": "selection",
            },
        }
        model_larpem_system_point = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
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
