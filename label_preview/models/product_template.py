from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_open_label_layout(self):
        print('--------------------------------in----product_product-------')
        import pdb;pdb.set_trace()
        # flake8: noqa: E501
        if not self.env['ir.config_parameter'].sudo().get_param('label_preview.replace_standard_wizard'):
            return super(ProductTemplate, self).action_open_label_layout()
        action = self.env['ir.actions.act_window']._for_xml_id('label_preview.action_print_label_from_template')
        action['context'] = {'default_product_template_ids': self.ids}
        return action
