# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import hashlib
import io
import json
import logging
import zipfile

import requests

from odoo import _, api, exceptions, fields, models, tools
from odoo.models import MAGIC_COLUMNS

_logger = logging.getLogger(__name__)
try:
    import odoorpc
except ImportError:  # pragma: no cover
    _logger.debug("Cannot import odoorpc")

MAGIC_FIELDS = MAGIC_COLUMNS + [
    "display_name",
    "__last_update",
    "access_url",
    "access_token",
    "access_warning",
    "activity_summary",
    "activity_ids",
    "message_follower_ids",
    "message_ids",
    "website_message_ids",
    "activity_type_id",
    "activity_user_id",
    "activity_state",
    "message_channel_ids",
    "message_main_attachment_id",
    "message_partner_ids",
    "activity_date_deadline",
    "message_attachment_count",
    "message_has_error",
    "message_has_error_counter",
    "message_is_follower",
    "message_needaction",
    "message_needaction_counter",
    "message_unread",
    "message_unread_counter",
]


class SyncDB(models.Model):
    _name = "larpem.sync.db"
    _inherit = "mail.thread"
    _description = "Sync odoo db"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        help="Summary of this backup process",
    )

    protocol = fields.Selection(
        selection=[
            ("http", "http"),
            ("https", "https"),
        ],
        default="https",
        required=True,
    )

    method_sync = fields.Selection(
        selection=[
            ("all", "All"),
            # ("white", "White"),
        ],
        default="all",
        help=(
            "If empty, sync all field. If all, sync all not system and not"
            " compute field."
        ),
    )

    sync_host = fields.Char(
        string="Sync Server",
        help=(
            "The host name or IP address from your remote server. For example"
            " 192.168.0.1"
        ),
    )

    module_name = fields.Char(
        string="Module name",
        help="Separate by ; for multiple module check.",
        default="larpem",
    )

    sync_password = fields.Char(
        string="Password",
        help="The password for the SYNC connection.",
    )

    sync_port = fields.Integer(
        string="HTTP Port",
        help="The port for http or https",
        default=443,
    )

    database = fields.Char(
        string="Database",
        help="Database name, set nothing to get default database.",
        default="tl_user.json",
    )

    sync_user = fields.Char(
        string="Username in the Sync Server",
        help=(
            "The username where the SYNC connection should be made with. This"
            " is the user on the external server."
        ),
    )

    sync_db_result_ids = fields.One2many(
        comodel_name="larpem.sync.db.result",
        inverse_name="sync_db_id",
        string="Sync DB Results",
    )

    @api.onchange("protocol")
    def _onchange_protocol(self):
        # update port
        if self.protocol == "http":
            self.sync_port = 80
        elif self.protocol == "https":
            self.sync_port = 443

    @api.multi
    @api.depends(
        "protocol",
        "sync_user",
        "sync_host",
        "database",
        "sync_port",
        "module_name",
    )
    def _compute_name(self):
        """Get the right summary for this job."""
        for rec in self:
            rec.name = (
                f"{rec.protocol}://{rec.sync_host}:{rec.sync_port} with"
                f" '{rec.sync_user}' DB '{rec.database}' MOD"
                f" '{rec.module_name}'"
            )

    @api.multi
    def action_sync_test_connection(self):
        error = ""
        for rec in self:
            try:
                url = f"{rec.protocol}://{rec.sync_host}"
                if rec.sync_port:
                    url += f":{rec.sync_port}"
                url += "/login"
                password = hashlib.sha256()
                password.update(rec.sync_password.encode())
                session = requests.Session()
                response = session.post(
                    url,
                    params={
                        "username_or_email": rec.sync_user,
                        "password": password.hexdigest(),
                    },
                    auth=(rec.sync_user, password.hexdigest()),
                )
                if response.url != url.replace("login", "profile"):
                    error = _("Connexion seems not correct.")
            except Exception as e:
                error = _("Cannot connect : ") + str(e)

        if error:
            _logger.error("Error sync connexion test")
            raise exceptions.Warning(_("FAILED - Sync connexion : ") + error)
        else:
            _logger.info("Succeed sync connexion test")
            raise exceptions.Warning(_("SUCCEED - Sync connexion"))

    def get_bd(self, rec):
        try:
            url = f"{rec.protocol}://{rec.sync_host}"
            if rec.sync_port:
                url += f":{rec.sync_port}"
            host = url
            url += "/login"
            password = hashlib.sha256()
            password.update(rec.sync_password.encode())
            session = requests.Session()
            response = session.post(
                url,
                params={
                    "username_or_email": rec.sync_user,
                    "password": password.hexdigest(),
                },
                auth=(rec.sync_user, password.hexdigest()),
            )
            if response.url != url.replace("login", "profile"):
                raise exceptions.Warning(_("Connexion seems not correct."))
        except Exception as e:
            raise exceptions.Warning(_("Cannot connect : ") + str(e))

        if not rec.database:
            raise exceptions.Warning(_("Missing database information"))
        url = f"{host}/cmd/admin/download_database?name={rec.database}"
        response = session.get(url)
        # Vérifier si la requête s'est correctement exécutée
        if response.status_code == 200:
            # Extraire le contenu du fichier zip
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))

            # Rechercher le fichier JSON dans le zip (vous pouvez adapter le nom du fichier si nécessaire)
            json_file_name = None
            for file_name in zip_file.namelist():
                if file_name.endswith(".json"):
                    json_file_name = file_name
                    break

            # Vérifier si le fichier JSON a été trouvé dans le zip
            if json_file_name:
                # Extraire le fichier JSON
                extracted_json = zip_file.extract(json_file_name)

                # Lire le contenu du fichier JSON
                with open(extracted_json, "r") as file:
                    json_data = json.load(file)

                # Fermer le fichier JSON extrait
                zip_file.close()
            else:
                raise exceptions.Warning(
                    _("Aucun fichier JSON trouvé dans le fichier zip.")
                )
        else:
            raise exceptions.Warning(
                _("Échec de la requête pour télécharger la page web.")
            )
        return json_data

    @api.multi
    def action_sync(self):
        """Run selected sync."""
        for rec in self:
            rec.sync_db_result_ids = [(5,)]
            # action_sync_test_connection()
            data_larpem = self.get_bd(rec)
            # Import user data
            db_user = data_larpem.get("_default")
            for bd_id, dct_user in db_user.items():
                name = dct_user.get("name")
                email = dct_user.get("email")
                is_found = False
                partner_id = None
                if email:
                    user_id = self.env["res.users"].search(
                        [("login", "=", email)]
                    )
                    if not len(user_id):
                        data = {
                            "name": name,
                            "login": email,
                            "email": email,
                            # "groups_id": [
                            #     (6, 0, [self.env.ref("base.group_portal").id])
                            # ],
                        }
                        self.env["larpem.sync.db.result"].create(
                            {
                                "sync_db_id": rec.id,
                                "type_result": "missing_result",
                                "msg": f"Missing res.users",
                                "model_name": "res.users",
                                "data": data,
                                "source": "local",
                                "resolution": "solution_local",
                            }
                        )
                    else:
                        is_found = True
                        partner_id = user_id.partner_id
                else:
                    partner_id = self.env["res.partner"].search(
                        [("name", "=", name)]
                    )
                    if not partner_id:
                        data = {"name": name}
                        self.env["larpem.sync.db.result"].create(
                            {
                                "sync_db_id": rec.id,
                                "type_result": "missing_module",
                                "msg": f"Missing res.partner",
                                "model_name": "res.partner",
                                "data": data,
                                "source": "local",
                                "resolution": "solution_local",
                            }
                        )
                    else:
                        is_found = True
                if is_found and partner_id:
                    lst_char = dct_user.get("character")
                    if len(lst_char) == 1:
                        char = lst_char[0]
                        # char_value = {
                        #     "name": char.get("name", False),
                        #     "partner_id": partner_id.id,
                        # }
                        personnage_id = self.env["larpem.personnage"].search(
                            [("partner_id", "=", partner_id.id)]
                        )
                        # Usually, can support multiple personnage, but not this software
                        name = char.get("name", False)
                        if len(personnage_id) > 1:
                            for p in personnage_id:
                                if p.name == name:
                                    personnage_id = p

                        if name and not personnage_id:
                            self.env["larpem.sync.db.result"].create(
                                {
                                    "sync_db_id": rec.id,
                                    "type_result": "missing_result",
                                    "msg": f"Missing personnage",
                                    "model_name": "larpem.personnage",
                                    "data": name,
                                    "source": "local",
                                    "resolution": "solution_local",
                                }
                            )
                        elif name and personnage_id:
                            if personnage_id.name != name:
                                self.env["larpem.sync.db.result"].create(
                                    {
                                        "sync_db_id": rec.id,
                                        "type_result": "diff_value",
                                        "msg": (
                                            "Name is different, old"
                                            f" '{personnage_id.name}', new"
                                            f" '{name}'"
                                        ),
                                        "record_id": personnage_id.id,
                                        "field_name": "name",
                                        "model_name": "larpem.personnage",
                                        # "data": name,
                                        "field_value_local": personnage_id.name,
                                        "field_value_remote": name,
                                        "source": "local",
                                        "resolution": "solution_local",
                                    }
                                )
