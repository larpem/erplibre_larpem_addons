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

        # Add/Update Larpem Banque
        model_model = "larpem.banque"
        model_name = "larpem_banque"
        dct_model = {
            "description": "Banque",
        }
        dct_field = {
            "description": {
                "code_generator_sequence": 3,
                "field_description": "Description",
                "ttype": "char",
            },
            "name": {
                "code_generator_sequence": 2,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_larpem_banque = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Larpem Banque Compte
        model_model = "larpem.banque.compte"
        model_name = "larpem_banque_compte"
        dct_model = {
            "description": "Compte bancaire",
        }
        dct_field = {
            "banque_id": {
                "code_generator_sequence": 4,
                "field_description": "Banque",
                "relation": "larpem.banque",
                "ttype": "many2one",
            },
            "etat_compte": {
                "code_generator_sequence": 6,
                "default": "actif",
                "field_description": "État du compte",
                "required": True,
                "selection": (
                    "[('actif', 'Actif'), ('ferme', 'Fermé'), ('block',"
                    " 'Bloqué')]"
                ),
                "ttype": "selection",
            },
            "name": {
                "code_generator_compute": "_compute_name",
                "code_generator_sequence": 2,
                "field_description": "Name",
                "store": True,
                "ttype": "char",
            },
            "no_compte": {
                "code_generator_sequence": 3,
                "field_description": "Numéro de compte",
                "ttype": "char",
            },
            "nom_personnage": {
                "code_generator_sequence": 8,
                "field_description": "Nom personnage",
                "ttype": "char",
            },
            "personnage_id": {
                "code_generator_sequence": 9,
                "field_description": "Personnage",
                "help": "Est la personne responsable du compte",
                "relation": "larpem.personnage",
                "ttype": "many2one",
            },
            "personnage_secondaire_ids": {
                "code_generator_sequence": 10,
                "comment_before": """TODO nom_personnage_secondaire
TODO il faut faire un compute et prendre tous leurs noms
nom_personnage_secondaire = fields.Char(string=\"Nom personnage secondaire\",
related=\"personnage_secondaire_ids.name\")""",
                "field_description": "Personnage secondaire",
                "help": "Personne secondaire responsable du compte",
                "relation": "larpem.personnage",
                "ttype": "many2many",
            },
            "raison_etat_compte": {
                "code_generator_sequence": 7,
                "field_description": "Raison Etat Compte",
                "help": (
                    "La raison lorsque l'état de compte est fermé ou bloqué."
                ),
                "ttype": "char",
            },
            "total": {
                "code_generator_sequence": 11,
                "field_description": "Sommaire du compte",
                "ttype": "float",
            },
            "type_compte": {
                "code_generator_sequence": 5,
                "default": "membre",
                "field_description": "Type de compte",
                "required": True,
                "selection": "[('membre', 'Membre'), ('affaire', 'Affaire')]",
                "ttype": "selection",
            },
        }
        model_larpem_banque_compte = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code model
            lst_value = [
                {
                    "code": '''for r in self:
    r.name = f"{r.banque_id.name} - {r.personnage_id.name}"''',
                    "name": "_compute_name",
                    "decorator": '@api.depends("banque_id", "personnage_id")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_larpem_banque_compte.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Larpem Manuel
        model_model = "larpem.manuel"
        model_name = "larpem_manuel"
        dct_model = {
            "description": "Manuel utilisateur et administrateur",
        }
        dct_field = {
            "admin": {
                "code_generator_sequence": 5,
                "field_description": "Admin seulement",
                "help": (
                    "Cette information est seulement pour les organisateurs du"
                    " jeu."
                ),
                "ttype": "boolean",
            },
            "bullet_description": {
                "code_generator_sequence": 10,
                "field_description": "Bullet Description",
                "ttype": "char",
            },
            "description": {
                "code_generator_sequence": 9,
                "field_description": "Description",
                "ttype": "text",
            },
            "hide_player": {
                "code_generator_sequence": 16,
                "field_description": "Hide Player",
                "ttype": "boolean",
            },
            "key": {
                "code_generator_sequence": 6,
                "field_description": "Key",
                "ttype": "char",
            },
            "model": {
                "code_generator_sequence": 14,
                "field_description": "Model",
                "ttype": "char",
            },
            "name": {
                "code_generator_compute": "_compute_name",
                "code_generator_sequence": 2,
                "field_description": "Name",
                "store": True,
                "ttype": "char",
            },
            "parent_id": {
                "code_generator_sequence": 3,
                "field_description": "Parent",
                "relation": "larpem.manuel",
                "ttype": "many2one",
            },
            "point": {
                "code_generator_sequence": 15,
                "field_description": "Point",
                "ttype": "char",
            },
            "second_bullet_description": {
                "code_generator_sequence": 11,
                "field_description": "Second Bullet Description",
                "ttype": "char",
            },
            "sub_key": {
                "code_generator_sequence": 13,
                "field_description": "Sub Key",
                "ttype": "char",
            },
            "title": {
                "code_generator_sequence": 7,
                "field_description": "Title",
                "ttype": "char",
            },
            "title_html": {
                "code_generator_sequence": 8,
                "field_description": "Title Html",
                "ttype": "html",
            },
            "under_level_color": {
                "code_generator_sequence": 12,
                "field_description": "Under Level Color",
                "ttype": "char",
            },
        }
        model_larpem_manuel = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code model
            lst_value = [
                {
                    "code": '''for rec in self:
    if rec.title:
        rec.name = rec.title
    else:
        rec.name = "NO TITLE"''',
                    "name": "_compute_name",
                    "decorator": '@api.depends("title")',
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_larpem_manuel.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Larpem Personnage
        model_model = "larpem.personnage"
        model_name = "larpem_personnage"
        dct_model = {
            "description": "Personnage",
        }
        dct_field = {
            "name": {
                "code_generator_sequence": 2,
                "field_description": "Nom personnage",
                "ttype": "char",
            },
            "nom_joueur": {
                "code_generator_sequence": 3,
                "field_description": "Nom joueur",
                "ttype": "char",
            },
            "partner_id": {
                "code_generator_sequence": 4,
                "field_description": "Participant",
                "relation": "res.partner",
                "ttype": "many2one",
            },
        }
        model_larpem_personnage = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

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
                "help": (
                    "Formule is an algorithm in Javascript to calculate value."
                ),
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
                    "[('Attribut', 'Attribut'), ('Ressource', 'Ressource')]"
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

        # Added one2many field, many2one need to be create before add one2many
        model_model = "larpem.manuel"
        dct_field = {
            "enfant_id": {
                "field_description": "Enfant",
                "ttype": "one2many",
                "code_generator_sequence": 4,
                "relation": "larpem.manuel",
                "relation_field": "parent_id",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        model_model = "larpem.personnage"
        dct_field = {
            "compte_bancaire_ids": {
                "field_description": "Comptes bancaires",
                "ttype": "one2many",
                "code_generator_sequence": 5,
                "relation": "larpem.banque.compte",
                "relation_field": "personnage_id",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        # Generate view
        value_snippet = {
            "code_generator_id": code_generator_id.id,
            "controller_feature": "model_show_item_list",
            "enable_javascript": True,
            "model_name": "larpem.manuel",
            "name": "Larpem manuel",
            "snippet_type": "structure",
        }
        env["code.generator.snippet"].create(value_snippet)

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
