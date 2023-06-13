# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import ast
import logging

from odoo import _, api, exceptions, fields, models, tools

_logger = logging.getLogger(__name__)


class SyncDBResult(models.Model):
    _name = "larpem.sync.db.result"
    _description = "Sync db odoo result"
    _order = "sequence, id"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        help="Summary of sync result",
    )

    model_name = fields.Char()

    sequence = fields.Integer(default=5)

    field_name = fields.Char()

    record_id = fields.Integer()

    field_value_local = fields.Char()

    field_value_remote = fields.Char()

    msg = fields.Text()

    data = fields.Text()

    sync_db_id = fields.Many2one(
        comodel_name="larpem.sync.db",
        string="Sync DB",
        required=True,
        index=True,
        ondelete="cascade",
    )

    type_result = fields.Selection(
        selection=[
            ("missing_result", "Missing result"),
            ("missing_field", "Missing field"),
            ("missing_model", "Missing model"),
            ("missing_module", "Missing module"),
            ("module_wrong_version", "Module wrong version"),
            ("module_not_installed", "Module not installed"),
            ("diff_value", "Diff value"),
        ],
        help="Type of result detected.",
    )

    colored_line = fields.Selection(
        selection=[
            ("LightYellow", "Warning"),
            ("LightSalmon", "Error"),
            ("Gray", "Sync/not"),
        ],
        compute="_compute_colored_line",
        store=True,
    )

    status = fields.Selection(
        selection=[
            ("not_solve", "Non résolu"),
            ("not_solvable", "Non résoluble"),
            ("solved", "Résolu"),
            ("warning", "Warning"),
            ("error", "Error"),
        ],
        default="not_solve",
    )

    resolution = fields.Selection(
        selection=[
            ("solution_remote", "Solution remote"),
            ("solution_local", "Solution local"),
            ("solution_remote_local", "Solution remote et local"),
        ]
    )

    source = fields.Selection(
        selection=[
            ("local", "Local"),
            ("remote", "Remote"),
        ],
        help="The result affect local instance or remote instance?",
    )

    @api.multi
    @api.depends("model_name")
    def _compute_name(self):
        for rec in self:
            rec.name = rec.model_name

    @api.multi
    @api.depends("status")
    def _compute_colored_line(self):
        for rec in self:
            if rec.status == "not_solvable":
                rec.colored_line = "Gray"
            elif rec.status == "solved":
                rec.colored_line = "Gray"
            elif rec.status == "warning":
                rec.colored_line = "LightYellow"
            elif rec.status == "error":
                rec.colored_line = "LightSalmon"
            elif rec.status == "not_solve":
                rec.colored_line = False
            else:
                rec.colored_line = False

    @api.multi
    def sync_local(self):
        for rec in self:
            if rec.resolution not in [
                "solution_local",
                "solution_remote_local",
            ]:
                continue
            if rec.type_result == "missing_result":
                rec.status = "solved"
                data_v = ast.literal_eval(rec.data)
                # self.env[rec.model_name].create(ast.literal_eval(rec.data))
                data_larpem = rec.sync_db_id.get_bd(rec.sync_db_id)
                # Import user data
                partner_id = None
                db_user = data_larpem.get("_default")
                for bd_id, dct_user in db_user.items():
                    name = dct_user.get("name")
                    email = dct_user.get("email")
                    if rec.model_name == "res.users":
                        if data_v.get("email") == email:
                            data = {
                                "name": name,
                                "login": email,
                                "email": email,
                                "groups_id": [
                                    (
                                        6,
                                        0,
                                        [self.env.ref("base.group_portal").id],
                                    )
                                ],
                            }
                            user_id = (
                                self.env["res.users"]
                                .with_context({"no_reset_password": True})
                                .create(data)
                            )
                            partner_id = user_id.partner_id
                    elif rec.model_name == "res.partner":
                        if data_v.get("name") == name:
                            data = {
                                "name": name,
                            }
                            partner_id = self.env["res.partner"].create(data)
                    if partner_id:
                        lst_char = dct_user.get("character")
                        if len(lst_char) < 1:
                            raise exceptions.Warning(
                                f"User name {name} id {bd_id} missing"
                                " character"
                            )
                        elif len(lst_char) > 1:
                            raise exceptions.Warning(
                                f"User name {name} id {bd_id} has multiple"
                                " character, why?"
                            )
                        else:
                            char = lst_char[0]
                            char_value = {
                                "name": char.get("name", False),
                                "partner_id": partner_id.id,
                            }

                            self.env["larpem.personnage"].create(char_value)

                        zip_str = dct_user.get("postal_code")
                        if zip_str:
                            partner_id.zip = zip_str

                        rec.status = "solved"
                        break
                else:
                    raise exceptions.Warning(
                        _(f"Cannot find '{data_v}' from remote.")
                    )
            elif rec.type_result == "diff_value":
                setattr(
                    self.env[rec.model_name].browse(rec.record_id),
                    rec.field_name,
                    rec.field_value_remote,
                )
                rec.status = "solved"
            else:
                raise exceptions.Warning(
                    _(f"Cannot support type_result '{rec.type_result}'.")
                )

    @api.multi
    def sync_remote(self):
        raise exceptions.Warning(_(f"Not supported sync remote."))
