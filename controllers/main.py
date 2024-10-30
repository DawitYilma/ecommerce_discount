# controllers/inherited_shop.py

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route
from odoo.tools.json import scriptsafe as json_scriptsafe
from odoo.addons.payment import utils as payment_utils
import logging

_logger = logging.getLogger(__name__)


class InheritedWebsiteSale(WebsiteSale):
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        # Call the original shop method to get the base values
        response = super(InheritedWebsiteSale, self).shop(
            page=page, category=category, search=search, min_price=min_price, max_price=max_price, ppg=ppg, **post
        )

        # Add custom logic to calculate the discounted price
        products = response.qcontext['products']  # Access products from the original response
        discounted_prices = {}

        # Calculate the discounted price for each product
        for product in products:
            discount = product.discount_percentage or 0
            original_price = product.list_price

            #Add the discounted price to be displayed on the product template
            if discount > 0:
                discounted_price = original_price * (1 - discount / 100)
            else:
                discounted_price = original_price
            discounted_prices[product.id] = discounted_price

        # Update the response with the discounted prices
        response.qcontext['discounted_prices'] = discounted_prices

        return response
