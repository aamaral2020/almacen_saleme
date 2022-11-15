##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    price = fields.Monetary(
        compute='_compute_price2',
        help='Price for product specified on the context',
    )
    show_products = fields.Boolean(
        'Show in products',
        default=True,
        help="By selecting it allows you to display the pricelist "
        "with the price of that product in the products",
    )

    @api.depends_context('product_id', 'template_id')
    def _compute_price2(self):
        product_id = self._context.get('product_id', False)
        template_id = self._context.get('template_id', False)
        for rec in self:
            price = 0
            if product_id:
                price = self.env['product.product'].browse(
                    product_id).with_context(pricelist=rec.id).price
                rec.price = price
            elif template_id:
                prod = self.env['product.product'].search([('product_tmpl_id','=',template_id)])
                if len(prod) == 1:
                    price = prod.with_context(pricelist=rec.id).price
                    rec.price = price
                else:
                    rec.price = 0.0
            else:
                rec.price = 0.0
