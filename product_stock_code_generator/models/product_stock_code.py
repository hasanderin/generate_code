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
                continue
            seq = self.env['ir.sequence'].sudo().next_by_code(sequence_code)
            if not seq:
                raise UserError(_('Stok kodu için sıra (sequence) bulunamadı.'))
            template.stock_code = f"{prefix}{seq}"

    def action_open_stock_code_settings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Stok Kodu Ayarları'),
            'res_model': 'res.config.settings',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_stock_code_prefix': self.env['ir.config_parameter'].sudo().get_param('product_stock_code_generator.prefix', default='STK')},
        }

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            domain = ['|', '|', '|',
                      ('stock_code', operator, name),
                      ('default_code', operator, name),
                      ('barcode', operator, name),
                      ('name', operator, name)]
            return super()._name_search(name='', args=domain + args, operator=operator, limit=limit, name_get_uid=name_get_uid)
        return super()._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        # Defer to _name_search to keep behavior consistent across contexts
        ids = self._name_search(name=name, args=args, operator=operator, limit=limit)
        return self.browse(ids).name_get()

    def name_get(self):
        # Decorate display names with stock_code when present
        result = super().name_get()
        id_to_name = dict(result)
        for record in self:
            base = id_to_name.get(record.id)
            if base and record.stock_code:
                id_to_name[record.id] = f"{base} [{record.stock_code}]"
        return [(rid, name) for rid, name in id_to_name.items()]

    @api.model
    def create(self, vals):
        template = super().create(vals)
        return template

    def write(self, vals):
        return super().write(vals)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_code = fields.Char(
        related='product_tmpl_id.stock_code',
        readonly=False,
        store=True,
        index=True,
        copy=False,
        string='Stok Kodu'
    )

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            domain = ['|', '|', '|',
                      ('stock_code', operator, name),
                      ('default_code', operator, name),
                      ('barcode', operator, name),
                      ('name', operator, name)]
            return super()._name_search(name='', args=domain + args, operator=operator, limit=limit, name_get_uid=name_get_uid)
        return super()._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        ids = self._name_search(name=name, args=args, operator=operator, limit=limit)
        return self.browse(ids).name_get()

    def name_get(self):
        result = super().name_get()
        id_to_name = dict(result)
        for record in self:
            base = id_to_name.get(record.id)
            if base and record.stock_code:
                id_to_name[record.id] = f"{base} [{record.stock_code}]"
        return [(rid, name) for rid, name in id_to_name.items()]