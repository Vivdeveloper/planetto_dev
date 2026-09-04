import frappe
from frappe.utils import flt

from erpnext.controllers.status_updater import get_allowance_for
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt


class CustomPurchaseReceipt(PurchaseReceipt):
	"""Allow CEO to submit GRN when received qty exceeds Purchase Order qty."""

	def check_overflow_with_allowance(self, item, args):
		qty_or_amount = "qty" if "qty" in args["target_ref_field"] else "amount"

		if qty_or_amount != "qty" or args.get("overflow_type") != "receipt":
			return super().check_overflow_with_allowance(item, args)

		if not _user_has_ceo_role():
			return super().check_overflow_with_allowance(item, args)

		(
			allowance,
			self.item_allowance,
			self.global_qty_allowance,
			self.global_amount_allowance,
		) = get_allowance_for(
			item["item_code"],
			self.item_allowance,
			self.global_qty_allowance,
			self.global_amount_allowance,
			qty_or_amount,
		)

		overflow_percent = (
			(item[args["target_field"]] - item[args["target_ref_field"]])
			/ item[args["target_ref_field"]]
		) * 100

		if overflow_percent - allowance > 0.01:
			item["max_allowed"] = flt(item[args["target_ref_field"]] * (100 + allowance) / 100)
			item["reduce_by"] = item[args["target_field"]] - item["max_allowed"]
			self.warn_about_bypassing_with_role(item, qty_or_amount, "CEO")
			return

		return super().check_overflow_with_allowance(item, args)


def _user_has_ceo_role() -> bool:
	if frappe.session.user == "Administrator":
		return True
	return "CEO" in frappe.get_roles()
