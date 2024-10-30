# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo import osv
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    discount_percentage = fields.Float(string='Discount', default=0)