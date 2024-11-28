import base64
from io import BytesIO
import xlsxwriter
from odoo import models, fields
from odoo.tools import format_date

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def action_export_to_excel(self):
        active_ids = self.env.context.get('active_ids')
        if not active_ids:
            return False
        pickings = self.env['stock.picking'].browse(active_ids)

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Stock Pickings")
        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})
        sheet.merge_range(0, 0, 0, 5, "Stock Picking Report", title_format)

        headers = ['Reference', 'Scheduled Date', 'Partner', 'State', 'Operation Type', 'Created By']
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'align': 'center'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'align': 'center'})
        for col, header in enumerate(headers):
            sheet.write(1, col, header, header_format)
            sheet.set_column(col, col, 20)  # Set column width

        row = 2
        for picking in pickings:
            sheet.write(row, 0, picking.name or "")
            sheet.write(row, 1, format_date(self.env, picking.scheduled_date) if picking.scheduled_date else "", date_format)
            sheet.write(row, 2, picking.partner_id.name or "")
            sheet.write(row, 3, picking.state or "")
            sheet.write(row, 4, picking.picking_type_id.name or "") 
            sheet.write(row, 5, picking.create_uid.name or "")  
            row += 1

        workbook.close()
        output.seek(0)

        
        attachment = self.env['ir.attachment'].create({
            'name': 'Stock_Pickings_Report.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': 'stock.picking',
            'res_id': pickings[0].id if pickings else False,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        output.close()

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
