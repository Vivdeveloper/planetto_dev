import frappe


def execute():
	"""Ensure CEO role exists for GRN over-qty submit permission."""
	if frappe.db.exists("Role", "CEO"):
		return

	frappe.get_doc({"doctype": "Role", "role_name": "CEO", "desk_access": 1}).insert(
		ignore_permissions=True
	)
