# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ORMSafeModel(models.Model):
    """A model to test ORM safety and compute methods."""

    _name = "orm.safe.model"
    _description = "ORM Safety Test Model"

    name = fields.Char(required=True)
    is_active = fields.Boolean(default=True)

    # Correctly defined compute field with dependencies
    related_name = fields.Char(
        string="Computed Name",
        compute="_compute_related_name",
        store=True,
    )

    @api.depends("name")
    def _compute_related_name(self):
        """Compute the related name by prefixing."""
        for record in self:
            message = _("SAFE: ")
            record.related_name = message + record.name

    def action_perform_safe_update(self):
        """
        Demonstrates safe batch writing (preferred over record-by-record update).
        (Avoids linting error for unnecessary ORM loop).
        """
        # This is safe and efficient
        self.write({"is_active": False})
        return True

    def _execute_safe_sql(self):
        """
        Demonstrates safe SQL execution using parameters.
        (Avoids linting error for sql-injection).
        """
        self.ensure_one()
        # The 'id' placeholder prevents SQL injection
        query = "SELECT name FROM orm_safe_model WHERE id = %s"
        self.env.cr.execute(query, (self.id,))
        result = self.env.cr.fetchone()

        if not result:
            raise UserError(_("Record not found via SQL."))

        return result[0]
