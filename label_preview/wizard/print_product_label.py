# Copyright © 2025 Inwizards (<https://www.inwizards.com/>)
# @author: Ravi (<support@inwizards.in>)
# @author: Vishal (<support@inwizards.in>>)
# License LGPL-3.0 or later (https://www.khlkl/lgpl-3.0.html).

import base64
from typing import List

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_partner import _lang_get

class PrintProductLabel(models.TransientModel):
    _name = "print.product.label"
    _description = 'Wizard to print Product Labels'
    
    
    # added code by ravi------------
    
    # New field for custom barcode template
    # custom_template_id = fields.Many2one(
    #     comodel_name='product.label.template', 
    #     string='Custom Template',
    #     help="Select a custom template for the product label."
    # )
    
    custom_tmp_id = fields.Many2one(
        comodel_name='ir.actions.report', 
        string='Custom Template tmp id',
        help="Select a custom template for the product label."
    )
    zpl_template = fields.Text(string="ZPL Template")

    custom_template_id = fields.Many2one(
        'ir.actions.report',  # Replace this with the correct model name
        string="Custom Template12",
    )
    # custom_template_id = fields.Many2one(
    #     'custom.label.template',  # Replace this with the correct model name
    #     string="Custom Template",
    #     domain="[('model', '=', 'print.product.label.line')]"
    # )
    # added code by ravi------------




    @api.model
    def _complete_label_fields(self, label_ids: List[int]) -> List[int]:
        """Set additional fields for product labels. Method to override."""
        # Increase a label sequence
        labels = self.env['print.product.label.line'].browse(label_ids)
        for seq, label in enumerate(labels):
            label.sequence = 1000 + seq
        return label_ids

    @api.model
    def _get_product_label_ids(self):
        res = []
        # flake8: noqa: E501
        if self._context.get('active_model') == 'product.template':
            products = self.env[self._context.get('active_model')].browse(
                self._context.get('default_product_template_ids')
            )
            for product in products:
                label = self.env['print.product.label.line'].create({
                    'product_id': product.product_variant_id.id,
                })
                res.append(label.id)
        elif self._context.get('active_model') == 'product.product':
            products = self.env[self._context.get('active_model')].browse(
                self._context.get('default_product_product_ids')
            )
            for product in products:
                label = self.env['print.product.label.line'].create({'product_id': product.id})
                res.append(label.id)
        res = self._complete_label_fields(res)
        return res

    @api.model
    def default_get(self, fields_list):
        default_vals = super(PrintProductLabel, self).default_get(fields_list)
        if 'label_type_id' in fields_list and not default_vals.get('label_type_id'):
            default_vals['label_type_id'] = self.env.ref('label_preview.type_product').id
        return default_vals

    name = fields.Char(default='Print Product Labels')
    message = fields.Char(readonly=True)
    output = fields.Selection(selection=[('pdf', 'PDF')], string='Print to', default='pdf')
    mode = fields.Selection(
        selection=[('product.product', 'Products')],
        help='Technical field to specify the mode of the label printing wizard.',
        default='product.product',
    )
    label_type_id = fields.Many2one(comodel_name='print.label.type', string='Label Type')
    label_ids = fields.One2many(
        comodel_name='print.product.label.line',
        inverse_name='wizard_id',
        string='Labels for Products',
        default=_get_product_label_ids,
    )
    report_id = fields.Many2one(
        comodel_name='ir.actions.report',
        string='Label',
        domain=[('model', '=', 'print.product.label.line')],
    )
    is_template_report = fields.Boolean(compute='_compute_is_template_report')
    qty_per_product = fields.Integer(
        string='Label quantity per product',
        default=1,
    )
    # Options
    humanreadable = fields.Boolean(
        string='Human readable barcode',
        help='Print digital code of barcode.',
        default=False,
    )
    border_width = fields.Integer(
        string='Border',
        help='Border width for labels (in pixels). Set "0" for no border.'
    )
    lang = fields.Selection(
        selection=_lang_get,
        string='Language',
        help="The language that will be used to translate label names.",
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        help='Specify a company for product labels.'
    )
    # extra_html = fields.Html('Extra Content', default='')   # add by ravi
    # action_print = fields.Char(string="Action Print")       # add by ravi
    pdf = fields.Binary('PDF')               # add by ravi
    # barcode_preview = fields.Html()       # add by ravi
    barcode_preview = fields.Html('Barcode Preview', default="", readonly=True)       # add by ravi
    is_custom_tmpl = fields.Boolean(string="Custom Template222", default=False)          # add by ravi
    
    
    @api.onchange('custom_template_id')
    def _onchange_custom_template_id(self):
        print('----------------------------------------------')
        # import pdb;pdb.set_trace()
        if self.custom_template_id:
            self.action_show_preview()
            
            
    
    def _prepare_report_data(self):
        
    
        # if self.custom_quantity <= 0:
        #     raise UserError(_('You need to set a positive quantity.'))

        # Get layout grid
        # if self.report_id.name == 'Product Label from your own template':
        #     xml_id = 'product.report_product_template_label_dymo'
        # elif 'x' in self.print_format:
        #     xml_id = 'product.report_product_template_label_%sx%s' % (self.columns, self.rows)
        #     if 'xprice' not in self.print_format:
        #         xml_id += '_noprice'
        # else:
        # xml_id = "label_preview.action_report_product_label_50x38"
        xml_id = "product.report_product_template_label_dymo"

        active_model = 'product.product'
        products = ''
        for line in self.label_ids:
            products = line.product_id.ids
        # if self.product_tmpl_ids:
        #     products = self.product_tmpl_ids.ids
        #     active_model = 'product.template'
        # elif self.product_ids:
        #     products = self.product_ids.ids
        #     active_model = 'product.product'
        # else:
        #     raise UserError(_("No product to print, if the product is archived please unarchive it before printing its label."))

        # Build data to pass to the report  self.label_ids.wizard_id.id
        # import pdb;pdb.set_trace()
        layout_id = self.env["product.label.layout"].search([], limit=1)
        data = {
            'active_model': active_model,
            'quantity_by_product': {p: 3 for p in products},
            # 'layout_wizard': self.id,
            'layout_wizard': layout_id.id,  
            # 'price_included': 'xprice' in self.print_format,
            'price_included': False,
        }
        return xml_id, data
    
    
    def action_show_preview(self):
        # import pdb;pdb.set_trace()
        # if self.custom_template_id :
        #     self.report_id = self.custom_template_id
        # Prepare the report object
        
        #-added by ravi-----------------------------
        if self.custom_template_id.exists():
            self.report_id = self.custom_template_id
        #-added by ravi-----------------------------
        
        report = self.with_context(print_mode='html')._prepare_report()
        
        # Render the HTML content
        html_data = report._render_qweb_html(report, *self._get_report_action_params())
        
        # Check if the result is a tuple
        if isinstance(html_data, tuple):
         
            html_data = html_data[0]
        
        # Decode bytes to string if necessary
        if isinstance(html_data, bytes):
            html_data = html_data.decode('utf-8')

        # Optional: Clean up the HTML content
        cleaned_html = html_data.strip()

        # Save the cleaned HTML to the field
        self.barcode_preview = cleaned_html
        # import pdb;pdb.set_trace()
        '''report = self.with_context(print_mode='html')._prepare_report()
        report = self.env['ir.actions.report']._render_qweb_pdf(report, *self._get_report_action_params())[0]
        pdf = base64.encodebytes(report)
        self.pdf = pdf
        return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }'''
                
                
# -----------------------added by ravi--------------------------
    # def action_add_template(self):
    #     print('----------in main function')
    #     import pdb;pdb.set_trace()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Add Custom Label Template',
    #         'res_model': 'custom.label.template',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'target': 'new',  # This opens the form in a popup
    #     }
    def action_add_template(self):
        print('----------in main function')
        # import pdb;pdb.set_trace()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Custom Label Template',
            'res_model': 'ir.actions.report',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',  # This opens the form in a popup
            'context':{ 'default_model':'print.product.label.line',
            'default_is_custom_template':True}
           
        }
        
        
        
            
        
# -----------------------added by ravi--------------------------


    @api.depends('report_id')
    def _compute_is_template_report(self):
        for wizard in self:
            # flake8: noqa: E501
            wizard.is_template_report = self.report_id == self.env.ref('label_preview.action_report_product_label_from_template')

    def get_labels_to_print(self):
        self.ensure_one()
        labels = self.label_ids.filtered(lambda l: l.selected and l.qty)
        if not labels:
            raise UserError(_('Nothing to print, set the quantity of labels in the table.'))
        return labels

    def _get_report_action_params(self):
        """Return two params for a report action: record "ids" and "data"."""
        self.ensure_one()
        return self.get_labels_to_print().ids, None

    def _prepare_report(self):
        self.ensure_one()
        output_mode = self._context.get('print_mode', 'pdf')
        if not self.report_id:
            raise UserError(_('Please select a label type.'))
        report = self.report_id.with_context(discard_logo_check=True, lang=self.lang)
        report.sudo().write({'report_type': f'qweb-{output_mode}'})
        return report
    


    def action_print(self):
        print('-------------i am in action funciton-----------')
        # import pdb;pdb.set_trace()
        #-added by ravi-----------------------------
        if self.custom_template_id.exists():
            self.report_id = self.custom_template_id
        #-added by ravi-----------------------------
            
        self.ensure_one()
        report = self._prepare_report()
        report_template = report.report_action(*self._get_report_action_params())
        return report_template
        
 
       

    def action_set_qty(self):
        """Set a specific number of labels for all lines."""
        self.ensure_one()
        self.label_ids.write({'qty': self.qty_per_product})

    def action_restore_initial_qty(self):
        """Restore the initial number of labels for all lines."""
        self.ensure_one()
        for label in self.label_ids:
            if label.qty_initial:
                label.update({'qty': label.qty_initial})

    @api.model
    def get_quick_report_action(
            self, model_name: str, ids: List[int], qty: int = None, template=None, force_direct: bool = False,
    ):
        print('------------==================----------')
        import pdb;pdb.set_trace()
        """ Allow to get a report action for custom labels. Method to override. """
        wizard = self.with_context(
            **{'active_model': model_name, f'default_{model_name.replace(".", "_")}_ids': ids}
        ).create({'report_id': self.env.ref('label_preview.action_report_product_label_50x38').id})
        return wizard.action_print()

    @api.model
    def _set_sequence(self, lbl, seq, processed):
        if lbl in processed:
            return seq, processed
        lbl.sequence = seq
        seq += 1
        processed += lbl
        return seq, processed

    def action_sort_by_product(self):
        self.ensure_one()
        sequence = 1000
        processed_labels = self.env['print.product.label.line'].browse()
        # flake8: noqa: E501
        for label in self.label_ids:
            sequence, processed_labels = self._set_sequence(label, sequence, processed_labels)
            tmpl_labels = self.label_ids.filtered(lambda l: l.product_id.product_tmpl_id == label.product_id.product_tmpl_id).sorted(lambda l: l.product_id.id, reverse=True) - label
            for tmpl_label in tmpl_labels:
                sequence, processed_labels = self._set_sequence(tmpl_label, sequence, processed_labels)
                product_labels = tmpl_labels.filtered(lambda l: l.product_id == label.product_id) - tmpl_label
                for product_label in product_labels:
                    sequence, processed_labels = self._set_sequence(product_label, sequence, processed_labels)

    def get_pdf(self):
        self.ensure_one()
        print('-------pdf--------')
        import pdb;pdb.set_trace()
        report = self.with_context(print_mode='pdf')._prepare_report()
        pdf_data = report._render_qweb_pdf(report, *self._get_report_action_params())
        return base64.b64encode(pdf_data[0])



#added by ravi----------------------
    def generate_labels(self):
        print('-------------adding- preview ----------')
        import pdb;pdb.set_trace()
        for record in self:
            if record.custom_template_id:
                custom_template = record.custom_template_id
                # Generate report with custom_template.html_code
                return self.env.ref('label_preview.action_report_custom_product_label').report_action(self)
            

class ProductLabelTemplate(models.Model):
    _name = "product.label.template"
    _description = "Custom Product Label Template"

    name = fields.Char(string="Template Name", required=True)
    template_code = fields.Text(string="Template Code", required=True, help="QWeb template code for the label.")
    active = fields.Boolean(default=True)
    

class ProductLabelTemplate(models.Model):
    _inherit = "ir.actions.report"   
     
    is_custom_template = fields.Boolean(string="Custom Template333")  
    # custom_report = fields.Many2many('ir.action.report')  
#added by ravi----------------------
    
    
    def create(self,vals):
        # print("i am in create function")
        # import pdb;pdb.set_trace()
        
        return super(ProductLabelTemplate,self).create(vals)


