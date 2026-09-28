from erpnext.projects.doctype.timesheet.timesheet import Timesheet

class CustomTimesheet(Timesheet):

    def validate_overlap_for(self, *args, **kwargs):
        # Disable overlap validation completely
        return
    def set_dates(self):
        """
        Bypass standard date validation
        """
        pass
