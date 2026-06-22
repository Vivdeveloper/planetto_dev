# Copyright (c) 2026, sanket and contributors
# For license information, please see license.txt

import calendar
from datetime import date

import frappe
from frappe import _

VIEW_MONTHLY = "Monthly Order Booking"
VIEW_YEARLY_MONTHLY = "Yearly Monthly Summary"
VIEW_CUSTOMER = "Customer Wise"
VIEW_CATEGORY = "Category Wise"
VIEW_SEGMENT = "Segment Wise"

MONTH_NAMES = [
	"",
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December",
]


def execute(filters=None):
	filters = filters or {}
	view_type = filters.get("view_type") or VIEW_YEARLY_MONTHLY

	columns = get_columns(view_type)
	data = get_data(filters, view_type)
	chart = get_chart(data, view_type, filters)
	report_summary = get_report_summary(filters)
	skip_total_row = view_type == VIEW_MONTHLY

	return columns, data, None, chart, report_summary, skip_total_row


def get_columns(view_type):
	if view_type == VIEW_MONTHLY:
		return [
			{"fieldname": "order_booking", "label": _("Order Booking"), "fieldtype": "Link", "options": "Order Booking", "width": 180},
			{"fieldname": "posting_date", "label": _("Posting Date"), "fieldtype": "Date", "width": 120},
			{"fieldname": "customer", "label": _("Customer"), "fieldtype": "Link", "options": "Customer", "width": 150},
			{"fieldname": "customer_name", "label": _("Customer Name"), "fieldtype": "Data", "width": 250},
			{"fieldname": "po_no", "label": _("PO No"), "fieldtype": "Data", "width": 150},
			{"fieldname": "description", "label": _("Description"), "fieldtype": "Small Text", "width": 250},
			{"fieldname": "amount", "label": _("Amount"), "fieldtype": "Currency", "width": 120},
			{"fieldname": "industries", "label": _("Segment"), "fieldtype": "Data", "width": 120},
			{"fieldname": "category", "label": _("Category"), "fieldtype": "Data", "width": 150},
		]

	if view_type == VIEW_YEARLY_MONTHLY:
		return [
			{"fieldname": "month", "label": _("Month"), "fieldtype": "Data", "width": 140},
			{"fieldname": "order_count", "label": _("No. of Orders"), "fieldtype": "Int", "width": 120},
			{"fieldname": "amount", "label": _("Amount"), "fieldtype": "Currency", "width": 140},
		]

	if view_type == VIEW_CUSTOMER:
		return [
			{"fieldname": "customer", "label": _("Customer"), "fieldtype": "Link", "options": "Customer", "width": 160},
			{"fieldname": "customer_name", "label": _("Customer Name"), "fieldtype": "Data", "width": 250},
			{"fieldname": "order_count", "label": _("No. of Orders"), "fieldtype": "Int", "width": 120},
			{"fieldname": "amount", "label": _("Amount"), "fieldtype": "Currency", "width": 140},
		]

	if view_type == VIEW_CATEGORY:
		return [
			{"fieldname": "category", "label": _("Category"), "fieldtype": "Data", "width": 180},
			{"fieldname": "order_count", "label": _("No. of Orders"), "fieldtype": "Int", "width": 120},
			{"fieldname": "amount", "label": _("Amount"), "fieldtype": "Currency", "width": 140},
		]

	if view_type == VIEW_SEGMENT:
		return [
			{"fieldname": "segment", "label": _("Segment"), "fieldtype": "Data", "width": 180},
			{"fieldname": "order_count", "label": _("No. of Orders"), "fieldtype": "Int", "width": 120},
			{"fieldname": "amount", "label": _("Amount"), "fieldtype": "Currency", "width": 140},
		]

	return []


def get_data(filters, view_type):
	where_clause, values = build_where_clause(filters)
	if where_clause is None:
		return []

	if view_type == VIEW_MONTHLY:
		return get_monthly_detail_data(where_clause, values)
	if view_type == VIEW_YEARLY_MONTHLY:
		return get_yearly_monthly_data(filters, where_clause, values)
	if view_type == VIEW_CUSTOMER:
		return get_grouped_data(where_clause, values, "customer", "customer_name")
	if view_type == VIEW_CATEGORY:
		return get_grouped_data(where_clause, values, "category")
	if view_type == VIEW_SEGMENT:
		return get_grouped_data(where_clause, values, "industries", label_field="segment")

	return []


def build_where_clause(filters):
	conditions = ["ob.docstatus < 2"]
	values = {}

	year = filters.get("year")
	month = filters.get("month") if year else None
	view_type = filters.get("view_type") or VIEW_YEARLY_MONTHLY

	if view_type in (VIEW_MONTHLY, VIEW_YEARLY_MONTHLY) and not year:
		return None, None

	if year:
		year_int = int(year)
		if month:
			month_int = _month_to_int(month)
			if not month_int:
				return None, None
			from_date, to_date = _month_date_range(year_int, month_int)
		else:
			from_date, to_date = date(year_int, 1, 1), date(year_int, 12, 31)
		conditions.append("ob.posting_date between %(from_date)s and %(to_date)s")
		values["from_date"] = from_date
		values["to_date"] = to_date

	if filters.get("customer"):
		conditions.append("ob.customer = %(customer)s")
		values["customer"] = filters["customer"]

	if filters.get("category"):
		conditions.append("ob.category = %(category)s")
		values["category"] = filters["category"]

	if filters.get("segment"):
		conditions.append("ob.industries = %(segment)s")
		values["segment"] = filters["segment"]

	return " AND ".join(conditions), values


def get_monthly_detail_data(where_clause, values):
	doctype = "Order Booking"
	alias = "ob"
	table = f"`tab{doctype}`"

	select_exprs = [
		"ob.name as order_booking",
		_col(doctype, "posting_date", alias),
		_col(doctype, "customer", alias),
		_col(doctype, "customer_name", alias),
		_col(doctype, "po_no", alias),
		_col(doctype, "description", alias),
		_col(doctype, "amount", alias),
		_col(doctype, "industries", alias),
		_col(doctype, "category", alias),
	]

	rows = frappe.db.sql(
		f"""
		SELECT {", ".join(select_exprs)}
		FROM {table} ob
		WHERE {where_clause}
		ORDER BY ob.posting_date ASC, ob.name ASC
		""",
		values,
		as_dict=True,
	)

	return [
		{
			"order_booking": row.get("order_booking") or "",
			"posting_date": row.get("posting_date"),
			"customer": row.get("customer"),
			"customer_name": row.get("customer_name"),
			"po_no": row.get("po_no"),
			"description": row.get("description"),
			"amount": row.get("amount") or 0,
			"industries": row.get("industries"),
			"category": row.get("category"),
		}
		for row in rows
	]


def get_yearly_monthly_data(filters, where_clause, values):
	year = int(filters.get("year"))
	table = "`tabOrder Booking`"
	amount_expr = "COALESCE(ob.amount, 0)"

	rows = frappe.db.sql(
		f"""
		SELECT
			MONTH(ob.posting_date) as month_num,
			COUNT(ob.name) as order_count,
			SUM({amount_expr}) as amount
		FROM {table} ob
		WHERE {where_clause}
		GROUP BY MONTH(ob.posting_date)
		ORDER BY MONTH(ob.posting_date)
		""",
		values,
		as_dict=True,
	)

	row_map = {row.month_num: row for row in rows}
	data = []

	for month_num in range(1, 13):
		row = row_map.get(month_num)
		data.append(
			{
				"month": MONTH_NAMES[month_num],
				"order_count": row.order_count if row else 0,
				"amount": row.amount if row else 0,
			}
		)

	return data


def get_grouped_data(where_clause, values, group_field, name_field=None, label_field=None):
	table = "`tabOrder Booking`"
	amount_expr = "COALESCE(ob.amount, 0)"
	label_field = label_field or group_field

	select_name = f"MAX(ob.{name_field}) as {name_field}" if name_field else ""
	select_parts = [
		f"ob.{group_field} as {label_field}",
		"COUNT(ob.name) as order_count",
		f"SUM({amount_expr}) as amount",
	]
	if select_name:
		select_parts.insert(1, select_name)

	rows = frappe.db.sql(
		f"""
		SELECT {", ".join(select_parts)}
		FROM {table} ob
		WHERE {where_clause}
		GROUP BY ob.{group_field}
		ORDER BY amount DESC, order_count DESC
		""",
		values,
		as_dict=True,
	)

	data = []
	for row in rows:
		entry = {
			label_field: row.get(label_field) or _("Not Specified"),
			"order_count": row.order_count or 0,
			"amount": row.amount or 0,
		}
		if name_field:
			entry[group_field] = row.get(group_field)
			entry[name_field] = row.get(name_field)
		else:
			entry[group_field] = row.get(label_field) or _("Not Specified")
		data.append(entry)

	return data


def get_chart(data, view_type, filters=None):
	filters = filters or {}

	if view_type == VIEW_MONTHLY:
		monthly_data = get_monthly_chart_data(filters)
		return build_monthly_bar_chart(monthly_data, filters)

	if not data:
		return None

	if view_type == VIEW_YEARLY_MONTHLY:
		return build_monthly_bar_chart(data, filters)

	label_field = {
		VIEW_CUSTOMER: "customer_name",
		VIEW_CATEGORY: "category",
		VIEW_SEGMENT: "segment",
	}.get(view_type)

	if not label_field:
		return None

	chart_rows = data[:20]
	return {
		"data": {
			"labels": [row.get(label_field) or _("Not Specified") for row in chart_rows],
			"datasets": [
				{"name": _("Amount"), "values": [row["amount"] for row in chart_rows]},
				{"name": _("No. of Orders"), "values": [row["order_count"] for row in chart_rows]},
			],
		},
		"type": "bar",
		"colors": ["#5e64ff", "#28a745"],
		"barOptions": {"spaceRatio": 0.5},
	}


def get_monthly_chart_data(filters):
	"""Monthly breakup for chart using the same filters as the report table."""
	if not filters.get("year"):
		return []

	where_clause, values = build_where_clause(filters)
	if where_clause is None:
		return []

	return get_yearly_monthly_data(filters, where_clause, values)


def get_filtered_totals(filters):
	view_type = filters.get("view_type") or VIEW_YEARLY_MONTHLY

	if view_type in (VIEW_MONTHLY, VIEW_YEARLY_MONTHLY) and not filters.get("year"):
		return 0, 0

	where_clause, values = build_where_clause(filters)
	if where_clause is None:
		return 0, 0

	result = frappe.db.sql(
		f"""
		SELECT
			COUNT(ob.name) as order_count,
			SUM(COALESCE(ob.amount, 0)) as amount
		FROM `tabOrder Booking` ob
		WHERE {where_clause}
		""",
		values,
		as_dict=True,
	)

	if not result:
		return 0, 0

	return result[0].order_count or 0, result[0].amount or 0


def build_monthly_bar_chart(monthly_data, filters=None):
	if not monthly_data:
		return None

	filters = filters or {}
	month_filter = filters.get("month")
	if month_filter and filters.get("year"):
		month_int = _month_to_int(month_filter)
		if month_int:
			monthly_data = [row for row in monthly_data if row["month"] == MONTH_NAMES[month_int]]

	if not monthly_data:
		return None

	return {
		"data": {
			"labels": [row["month"] for row in monthly_data],
			"datasets": [
				{"name": _("Amount"), "values": [row["amount"] for row in monthly_data]},
				{"name": _("No. of Orders"), "values": [row["order_count"] for row in monthly_data]},
			],
		},
		"type": "bar",
		"colors": ["#5e64ff", "#28a745"],
	}


def get_report_summary(filters):
	view_type = filters.get("view_type") or VIEW_YEARLY_MONTHLY

	if view_type in (VIEW_MONTHLY, VIEW_YEARLY_MONTHLY) and not filters.get("year"):
		return None

	total_orders, total_amount = get_filtered_totals(filters)

	return [
		{
			"value": total_orders,
			"label": _("Total Orders"),
			"datatype": "Int",
			"indicator": "Blue",
		},
		{
			"value": total_amount,
			"label": _("Total Amount"),
			"datatype": "Currency",
			"indicator": "Green",
		},
	]


def _month_date_range(year, month):
	first_day = date(year, month, 1)
	last_day = date(year, month, calendar.monthrange(year, month)[1])
	return first_day, last_day


def _month_to_int(month):
	if month is None:
		return None
	month_str = str(month).strip()
	if not month_str:
		return None
	if isinstance(month, int):
		return month
	if month_str.isdigit():
		return int(month_str)

	lookup = {name.lower(): index for index, name in enumerate(MONTH_NAMES) if name}
	return lookup.get(month_str.lower())


def _col(doctype, fieldname, alias):
	if frappe.db.has_column(doctype, fieldname):
		return f"{alias}.{fieldname} as {fieldname}"
	if fieldname == "amount":
		return "0 as amount"
	if fieldname == "posting_date":
		return "NULL as posting_date"
	return f"'' as {fieldname}"
