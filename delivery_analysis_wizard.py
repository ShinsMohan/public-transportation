from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DeliveryAnalysisWizard(models.TransientModel):
    _name = 'delivery.analysis.wizard'
    _description = "Delivery Analysis Report Wizard"

    start_date = fields.Date(string='Start Date', default=fields.Date.today)  
    end_date = fields.Date(string='End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='done',
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")
    group_customer = fields.Boolean(default=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError('End Date must be greater than Start Date.')

    def export_delivery_analysis_report(self):
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'state': self.state,
        }
        if self.group_customer:
            return self.env.ref('delivery_analysis_report.action_delivery_analysis_report_excel').report_action(self, data=data)
        else:
            return self.env.ref('delivery_analysis_report.action_detailed_delivery_analysis_report_excel').report_action(self, data=data)


