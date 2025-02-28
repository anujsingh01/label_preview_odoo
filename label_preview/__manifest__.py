# Copyright © 2025 Inwizards (<https://www.inwizards.com/>)
# @author: Ravi (<support@inwizards.in>)
# @author: Vishal (<support@inwizards.in>>)
# License LGPL-3.0 or later (https://www.khlkl/lgpl-3.0.html).

{
    'name': 'Custom Product Labels',
    'version': '17.0.1.3.2',
    'category': 'Extra Tools',
    'author': 'Inwizards',
    'website': '',
    'license': 'LGPL-3',
    'summary': 'Print custom product labels with barcode | Barcode Product Label',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'depends': [
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/product_data.xml',
        'data/print_label_type_data.xml',
        'report/product_label_reports.xml',
        'report/product_label_templates.xml',
        'wizard/print_product_label_views.xml',
        'views/res_config_settings_views.xml',
        
        # 'data/custom_barcode_template_data.xml',
        # 'views/custom_barcode_templates.xml',
        'views/custom_label_template_views.xml',
        'report/custom_label_report.xml',
        
    ],
    'assets': {
      'web.assets_backend': [
         '/label_preview/static/src/css/custom_css.css',
         ],
    },
     
    'demo': [
        'demo/product_demo.xml',
    ],
    'support': 'support@garazd.biz',
    'application': True,
    'installable': True,
    'auto_install': False,
}

