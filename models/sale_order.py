# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo import osv
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    #This method is used to add the discounted price to the price unit in the sale order
    def _cart_update_order_line(self, product_id, quantity, order_line, **kwargs):
        self.ensure_one()

        if order_line and quantity <= 0:
            # Remove zero or negative lines
            order_line.unlink()
            order_line = self.env['sale.order.line']
        elif order_line:
            # Update existing line
            update_values = self._prepare_order_line_update_values(order_line, quantity, **kwargs)

            #You calculate and add the discounted price in the dictionary
            product = self.env['product.template'].browse(order_line.product_id.id)
            if product.exists() and product.discount_percentage > 0:
                price_unit = product.list_price * (1 - (product.discount_percentage or 0) / 100)
                update_values['price_unit'] = price_unit
            if update_values:
                self._update_cart_line_values(order_line, update_values)
        elif quantity > 0:
            # Create new line
            order_line_values = self._prepare_order_line_values(product_id, quantity, **kwargs)

            #You calculate and add the discounted price in the dictionary
            product = self.env['product.template'].browse(order_line_values['product_id'])
            if product.exists() and product.discount_percentage > 0:
                price_unit = product.list_price * (1 - (product.discount_percentage or 0) / 100)
                order_line_values['price_unit'] = price_unit
            order_line = self.env['sale.order.line'].sudo().create(order_line_values)
            
        return order_line
