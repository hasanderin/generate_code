# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    stock_code_prefix = fields.Char(string='Stok Kodu Ön Eki', default='STK')

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'product_stock_code_generator.prefix', self.stock_code_prefix or ''
        )

    @api.model
    def get_values(self):
        res = super().get_values()
        prefix = self.env['ir.config_parameter'].sudo().get_param(
            'product_stock_code_generator.prefix', default='STK'
        )
        res.update(stock_code_prefix=prefix)
        return res