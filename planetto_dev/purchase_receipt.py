import frappe
from frappe import _
from frappe.utils import flt


def before_validate(doc, method=None):
	"""On GRN submit, only CEO can submit if qty or rate exceeds linked PO."""
	if getattr(doc, "_action", None) != "submit":
		return

	if doc.get("is_return"):
		return

	status = _get_submit_status(doc)
	if status.get("restricted"):
		frappe.throw(status["message"], title=_("CEO Role Required"))


@frappe.whitelist()
def get_submit_restriction(doc):
	"""Return exceed + whether current user is blocked from submit."""
	return _get_submit_status(doc)


@frappe.whitelist()
def get_po_comparison(doc):
	"""Return PO vs GRN comparison rows (role-independent)."""
	comparison = _build_comparison(doc)
	return comparison


def _get_submit_status(doc) -> dict:
	comparison = _build_comparison(doc)
	has_exceeded = bool(comparison.get("has_exceeded"))
	can_approve = _user_can_submit_increased_values()

	restricted = has_exceeded and not can_approve

	message = comparison.get("message") or ""
	if restricted and not message:
		message = _("Only users with CEO role can submit this GRN.")

	return {
		"restricted": restricted,
		"has_exceeded": has_exceeded,
		"can_approve": can_approve,
		"qty_items": comparison.get("qty_items") or [],
		"rate_items": comparison.get("rate_items") or [],
		"rows": comparison.get("rows") or [],
		"message": message,
	}


def _user_can_submit_increased_values() -> bool:
	if frappe.session.user == "Administrator":
		return True
	return "CEO" in frappe.get_roles()


def _build_comparison(doc) -> dict:
	if isinstance(doc, str):
		doc = frappe.parse_json(doc)

	# Client calls pass a dict; submit hooks pass a Document
	if isinstance(doc, dict):
		normalized = frappe._dict(doc)
		normalized.items = [frappe._dict(row) for row in (doc.get("items") or [])]
		return _get_restriction_status(normalized)

	return _get_restriction_status(doc)


def _get_restriction_status(doc) -> dict:
	if doc.get("is_return"):
		return {
			"has_exceeded": False,
			"qty_items": [],
			"rate_items": [],
			"rows": [],
			"message": "",
		}

	qty_items, rate_items, rows = _get_items_exceeding_po(doc)
	has_exceeded = bool(rows)

	parts = []
	if qty_items:
		parts.append(
			_("Quantity is increased beyond Purchase Order for item(s): {0}").format(
				", ".join(qty_items)
			)
		)
	if rate_items:
		parts.append(
			_("Rate is increased beyond Purchase Order for item(s): {0}").format(
				", ".join(rate_items)
			)
		)

	message = ""
	if has_exceeded:
		message = "{0}. {1}".format(
			" ".join(parts),
			_("Only users with CEO role can submit this GRN."),
		)

	return {
		"restricted": has_exceeded,
		"has_exceeded": has_exceeded,
		"qty_items": qty_items,
		"rate_items": rate_items,
		"rows": rows,
		"message": message,
	}


def _get_items_exceeding_po(doc) -> tuple:
	"""Return (qty_labels, rate_labels, comparison_rows) vs linked PO."""
	qty_increased = []
	rate_increased = []
	rows = []

	items = doc.get("items") or []
	po_item_names = [d.get("purchase_order_item") for d in items if d.get("purchase_order_item")]
	if not po_item_names:
		return qty_increased, rate_increased, rows

	po_map = {
		row.name: row
		for row in frappe.get_all(
			"Purchase Order Item",
			filters={"name": ["in", po_item_names]},
			fields=["name", "qty", "rate", "amount", "uom", "parent", "item_name"],
		)
	}

	for item in items:
		po_item = item.get("purchase_order_item")
		if not po_item:
			continue

		po_row = po_map.get(po_item)
		if not po_row:
			continue

		label = _item_label(item)
		po_qty = flt(po_row.qty)
		po_rate = flt(po_row.rate)
		grn_qty = flt(item.get("qty")) + flt(item.get("rejected_qty"))
		grn_rate = flt(item.get("rate"))

		qty_exceeded = grn_qty > po_qty
		rate_exceeded = grn_rate > po_rate

		if not (qty_exceeded or rate_exceeded):
			continue

		if qty_exceeded:
			qty_increased.append(label)
		if rate_exceeded:
			rate_increased.append(label)

		qty_diff = flt(grn_qty - po_qty)
		rate_diff = flt(grn_rate - po_rate)
		po_amount = flt(po_qty * po_rate)
		grn_amount = flt(grn_qty * grn_rate)
		amount_diff = flt(grn_amount - po_amount)

		qty_increase_pct = flt((qty_diff / po_qty) * 100) if po_qty else 0
		rate_increase_pct = flt((rate_diff / po_rate) * 100) if po_rate else 0

		if qty_exceeded and rate_exceeded:
			change_type = _("Qty & Rate")
		elif qty_exceeded:
			change_type = _("Qty")
		else:
			change_type = _("Rate")

		rows.append(
			{
				"idx": item.get("idx"),
				"item_code": item.get("item_code"),
				"item_name": item.get("item_name") or po_row.item_name or item.get("item_code"),
				"uom": item.get("uom") or po_row.uom or "",
				"purchase_order": po_row.parent or item.get("purchase_order"),
				"po_qty": po_qty,
				"grn_qty": grn_qty,
				"qty_diff": qty_diff,
				"qty_increase_pct": qty_increase_pct,
				"po_rate": po_rate,
				"grn_rate": grn_rate,
				"rate_diff": rate_diff,
				"rate_increase_pct": rate_increase_pct,
				"po_amount": po_amount,
				"grn_amount": grn_amount,
				"amount_diff": amount_diff,
				"qty_exceeded": qty_exceeded,
				"rate_exceeded": rate_exceeded,
				"change_type": change_type,
			}
		)

	return qty_increased, rate_increased, rows


def _item_label(item) -> str:
	idx = item.get("idx") or ""
	item_code = item.get("item_code") or ""
	return f"{item_code} (Row {idx})" if idx else item_code
