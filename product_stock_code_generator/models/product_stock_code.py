# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_code = fields.Char(
        string='Stok Kodu',
        copy=False,
        index=True,
        help='Ürün ve tüm varyantlar için ortak stok kodu.'
    )

    def action_generate_stock_code(self):
        IrConfig = self.env['ir.config_parameter'].sudo()
        prefix = IrConfig.get_param('product_stock_code_generator.prefix', default='STK')
        sequence_code = 'product.stock.code.generator'
        for template in self:
            if template.stock_code:
                # If already set, do not regenerate automatically
                continue
            seq = self.env['ir.sequence'].sudo().next_by_code(sequence_code)
            if not seq:
                raise UserError(_('Stok kodu için sıra (sequence) bulunamadı.'))
            template.stock_code = f"{prefix}{seq}"
            template.product_variant_ids.write({'stock_code': template.stock_code})

    @api.model
    def create(self, vals):
        template = super().create(vals)
        # If user provided stock_code manually, propagate to variants
        if vals.get('stock_code'):
            template.product_variant_ids.write({'stock_code': template.stock_code})
        return template

    def write(self, vals):
        res = super().write(vals)
        if 'stock_code' in vals:
            self.mapped('product_variant_ids').write({'stock_code': vals.get('stock_code')})
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_code = fields.Char(
        related='product_tmpl_id.stock_code',
        readonly=False,
        store=True,
        copy=False,
        string='Stok Kodu'
    )