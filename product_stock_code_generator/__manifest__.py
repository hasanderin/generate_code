# -*- coding: utf-8 -*-
{
    'name': 'Ürün Stok Kodu',
    'summary': 'Ürün ve varyantları için ortak stok kodu alanı ve otomatik üretim',
    'version': '15.0.1.0.0',
    'category': 'Inventory/Inventory',
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['product', 'stock'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/product_stock_code_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
}