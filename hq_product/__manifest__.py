# -*- coding: utf-8 -*-
{
    'name': "heqi_product",

    'summary': """
        产品重构""",
    'sequence': 15,
    'description': """
产品界面，功能重构
    """,

    'author': "heqiauto",
    'website': "http://www.yourcompany.com",

    'category': 'heqiauto',
    'version': '1.0',
    'depends': ['goods', 'core', 'sell', 'warehouse'],
    'data': [
        'views/insert_views.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/core_value.xml',
        'security/hq_auto_data.xml',
        'views/product_conf.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
