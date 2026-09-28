from erpnext.projects.doctype.timesheet.timesheet import Timesheet

class CustomTimesheet(Timesheet):

    def validate_overlap_for(self, *args, **kwargs):
        # Disable overlap validation completely
        return

    def set_dates(self):
        """
        Override the set_dates method to bypass the standard validation.
        """
        pass
		