# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class FleetVehicle(models.Model):
    _name = "fleet_vehicle"
    _inherit = ["mixin.master_data"]
    _description = "Fleet Vehicle"

    name = fields.Char(
        string="Vehicle",
    )
    code = fields.Char(
        string="License Plate",
    )
