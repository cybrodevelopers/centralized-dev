# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class LintTestModel(models.Model):
    """A standard model to demonstrate linting compliance."""

    _name = "lint.test.model"
    _description = "Lint Test Model"

    name = fields.Char(
        string="Name",
        required=True,
        help="The primary identifier for this record."
    )
    active = fields.Boolean(
        default=True,
        help="Set to False to hide this record without deleting it."
    )
    value = fields.Float(
        string="Value",
        digits=(10, 2)
    )
    description = fields.Text(
        string="Description"
    )

    @api.constrains('value')
    def _check_value(self):
        """Ensure the value is positive."""
        for record in self:
            if record.value < 0:
                raise UserError(_("The value must be positive."))

    def action_reset_value(self):
        """Reset the value to zero and log the action."""
        self.ensure_one()
        _logger.info("Resetting value for record %s", self.name)
        self.write({'value': 0.0})
        return True
