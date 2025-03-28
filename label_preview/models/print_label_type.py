from odoo import fields, models , api


class PrintLabelTypePy(models.Model):
    _name = "print.label.type"
    _description = 'Label Types'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)

    _sql_constraints = [('print_label_type_code_uniq', 'UNIQUE (code)', 'Code of a print label type must be unique.')]


#------add by ravi-------------------
class CustomLabelTemplate(models.Model):
    _name = 'custom.label.template'
    _description = 'Custom Label Template'

    name = fields.Char(string="Template Name", required=True)
    width = fields.Float(string="Label Width (mm)", required=True)
    height = fields.Float(string="Label Height (mm)", required=True)
    border_width = fields.Float(string="Border Width (px)", default=0)
    html_code = fields.Text(string="HTML Template")
    model = fields.Char(string="Model")

    # New fields for specifications
    paper_format = fields.Selection([
        ('a4', 'A4'),
        ('letter', 'Letter'),
        ('custom', 'Custom')
    ], string="Paper Format", required=True, default='a4')
    orientation = fields.Selection([
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape')
    ], string="Orientation", required=True, default='portrait')
    margin_top = fields.Float(string="Top Margin (mm)", default=0)
    margin_bottom = fields.Float(string="Bottom Margin (mm)", default=0)
    margin_left = fields.Float(string="Left Margin (mm)", default=0)
    margin_right = fields.Float(string="Right Margin (mm)", default=0)
    
    
    def action_add_template(self):
        # import pdb;pdb.set_trace()
        vals = {
            'name': self.name,  # Example field update
            'width': self.width,
            'height': self.height,
            'border_width': self.border_width,
            'html_code': self.html_code,
             'model': self.model,
            'paper_format': self.paper_format,
             'orientation': self.orientation,
            'margin_top': self.margin_top,
             'margin_bottom': self.margin_bottom,
            'margin_left': self.margin_left,
            'margin_right': self.margin_right,
             'display_name': self.display_name,
             'model': self.model, 
        }
        # Write method to update the current record
        self.write(vals)
        return {
            'type': 'ir.actions.act_window_close',
            'name': 'Add Custom Label Template',
            'res_model': 'custom.label.template',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',  # This opens the form in a popup
        }




    @api.model
    def create(self, vals):
        print('-i am in parent function------')
        import pdb;pdb.set_trace()
        # Call the original create method to create the custom.label.template record
        template = super(CustomLabelTemplate, self).create(vals)

        # Create the related print.product.label record
        self.env['print.product.label'].create({
            'custom_template_id': template.id,  # Link to the created custom.label.template
            'zpl_template': template.html_code or '',  # Example: Use the HTML code as ZPL Template
        })

        return template