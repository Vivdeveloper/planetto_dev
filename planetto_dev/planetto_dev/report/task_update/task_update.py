# Copyright (c) 2026, sanket and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 130,
		},
		{
			"label": _("Subject"),
			"fieldname": "parsed_subject",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("WO No"),
			"fieldname": "custom_wo_no",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("Expected Start Date"),
			"fieldname": "exp_start_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Expected End Date"),
			"fieldname": "exp_end_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Progress %"),
			"fieldname": "progress",
			"fieldtype": "Percent",
			"width": 110,
		},
		{
			"label": _("Expected Time (hours)"),
			"fieldname": "expected_time",
			"fieldtype": "Float",
			"width": 160,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("Task"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Task",
			"width": 200,
		},
	]


def parse_subject_before_dash(subject):
	"""Subject like 'VMM - PT1697IF' → 'VMM' (text before ' - ')."""
	if not subject:
		return ""
	s = subject.strip()
	sep = " - "
	if sep in s:
		return s.split(sep, 1)[0].strip()
	return s


def get_data(filters):
	conditions = ["task.docstatus < 2", "task.is_template = 0"]
	values = {}

	if filters.get("project"):
		conditions.append("task.project = %(project)s")
		values["project"] = filters["project"]

	if filters.get("company"):
		conditions.append("task.company = %(company)s")
		values["company"] = filters["company"]

	if filters.get("status"):
		conditions.append("task.status = %(status)s")
		values["status"] = filters["status"]

	if filters.get("from_date"):
		conditions.append("coalesce(task.exp_end_date, task.exp_start_date) >= %(from_date)s")
		values["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions.append("coalesce(task.exp_start_date, task.exp_end_date) <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	has_wo = frappe.db.has_column("Task", "custom_wo_no")
	if has_wo and filters.get("custom_wo_no"):
		conditions.append("task.custom_wo_no like %(custom_wo_no)s")
		values["custom_wo_no"] = f"%{filters['custom_wo_no']}%"

	where_clause = " AND ".join(conditions)

	wo_select = "task.custom_wo_no" if has_wo else "NULL as custom_wo_no"

	rows = frappe.db.sql(
		f"""
		SELECT
			task.name,
			task.project,
			task.subject,
			{wo_select},
			task.exp_start_date,
			task.exp_end_date,
			task.progress,
			task.expected_time,
			task.status
		FROM `tabTask` task
		WHERE {where_clause}
		ORDER BY task.project ASC, task.exp_start_date ASC, task.exp_end_date ASC, task.name ASC
		""",
		values,
		as_dict=True,
	)

	out = []
	for row in rows:
		out.append(
			{
				"name": row.name,
				"project": row.project,
				"parsed_subject": parse_subject_before_dash(row.subject),
				"custom_wo_no": row.get("custom_wo_no") or "",
				"exp_start_date": row.exp_start_date,
				"exp_end_date": row.exp_end_date,
				"progress": row.progress,
				"expected_time": row.expected_time,
				"status": row.status,
			}
		)

	return out
