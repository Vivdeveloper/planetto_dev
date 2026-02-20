
# import frappe

# def po_calculation_by_weight(doc, method=None):
#     """
#     Production-safe weight-based calculation for Purchase Order

#     Logic:
#     - total_weight becomes qty
#     - rate remains price per KG / per unit weight
#     - ERPNext calculates:
#         amount = qty × rate
#         taxes
#         totals
#         GL
#     """

#     # Debug confirmation
#     # frappe.msgprint("🔥 po_calculation_by_weight FIRED")

#     # Prevent infinite loop
#     if getattr(doc.flags, "weight_recalc_done", False):
#         return
#     doc.flags.weight_recalc_done = True

#     # Only apply when checkbox is checked
#     if not getattr(doc, "custom_calculate_based_on_weight", 0):
#         return

#     for item in doc.items:
#         try:
#             weight = float(item.total_weight or 0)

#             # Skip invalid rows
#             if weight <= 0:
#                 continue

#             # Store original qty once (for audit / revert)
#             if not item.get("custom_original_qty"):
#                 item.custom_original_qty = item.qty or 1

#             # ✅ CORE FIX — weight becomes quantity
#             item.qty = weight

#         except Exception:
#             continue

#     # Let ERPNext rebuild everything safely
#     try:
#         doc.calculate_taxes_and_totals()
#     except Exception:
#         pass




# import frappe

# def po_calculation_by_weight(doc, method):
#     # Run only if checkbox is ticked
#     if not doc.custom_calculate_based_on_weight:
#         return

#     for item in doc.items:
#         # Safety checks
#         if not item.rate:
#             continue

#         # If weight-based calculation
#         if item.total_weight:
#             item.amount = float(item.total_weight) * float(item.rate)
#         else:
#             # fallback (optional)
#             item.amount = float(item.qty) * float(item.rate)

#     # Proof popup (you asked for visible proof)
#     frappe.msgprint("✅ Weight based calculation applied (Server Script)")






# import frappe

# def po_calculation_by_weight(doc, method):
#     # Apply ONLY when checkbox is ticked
#     if not doc.custom_calculate_based_on_weight:
#         return

#     for item in doc.items:
#         # Safety: if rate missing, skip
#         if not item.rate:
#             item.amount = 0
#             continue

#         # STRICT weight-based calculation
#         # If total_weight is 0 or None → amount becomes 0
#         weight = float(item.total_weight or 0)
#         rate = float(item.rate)

#         item.amount = weight * rate   
    
#     # Proof popup
#     frappe.msgprint("✅ Strict weight-based calculation applied")

# import frappe

# def po_calculation_by_weight(doc, method):

#     company_currency = frappe.get_cached_value(
#         "Company", doc.company, "default_currency"
#     )

#     for item in doc.items:
#         try:
#             weight = float(item.total_weight or 0)
#             qty = float(item.qty or 1)
#             current_rate = float(item.rate or 0)
#         except Exception:
#             continue

#         # Skip if no rate
#         if current_rate <= 0:
#             item.amount = 0
#             continue

#         # Store original rate ONCE
#         if not item.custom_custom_rate or float(item.custom_custom_rate) == 0:
#             item.custom_custom_rate = current_rate

#         original_rate = float(item.custom_custom_rate)

#         # Normal pricing if no weight
#         if weight <= 0:
#             final_rate = original_rate
#         else:
#             final_rate = round(original_rate * weight, 2)

#         final_amount = round(final_rate * qty, 2)

#         # 🔥 SET ALL ERPNext TAX FIELDS
#         item.rate = final_rate
#         item.net_rate = final_rate
#         item.base_rate = final_rate
#         item.base_net_rate = final_rate

#         item.amount = final_amount
#         item.net_amount = final_amount
#         item.base_amount = final_amount
#         item.base_net_amount = final_amount
#         item.taxable_value = final_amount

#     frappe.msgprint("✅ GST now calculated on weighted amount")


# import frappe

# def po_calculation_by_weight(doc, method):

#     # 🔒 HARD GATE — Do nothing if checkbox is OFF
#     if not doc.custom_calculate_based_on_weight:
#         return

#     for item in doc.items:
#         try:
#             weight = float(item.total_weight or 0)
#             qty = float(item.qty or 1)
#             current_rate = float(item.rate or 0)
#         except Exception:
#             continue

#         # Skip if no rate
#         if current_rate <= 0:
#             item.amount = 0
#             continue

#         # 🧠 Store original rate ONCE
#         if not item.custom_custom_rate or float(item.custom_custom_rate) == 0:
#             item.custom_custom_rate = current_rate

#         original_rate = float(item.custom_custom_rate)

#         # Normal behavior if no weight
#         if weight <= 0:
#             final_rate = original_rate
#         else:
#             final_rate = round(original_rate * weight, 2)

#         final_amount = round(final_rate * qty, 2)

#         # 🔥 SET ALL ERPNext TAX FIELDS
#         item.rate = final_rate
#         item.net_rate = final_rate
#         item.base_rate = final_rate
#         item.base_net_rate = final_rate

#         item.amount = final_amount
#         item.net_amount = final_amount
#         item.base_amount = final_amount
#         item.base_net_amount = final_amount
#         item.taxable_value = final_amount
#         doc.total=final_amount

#     frappe.msgprint("✅ Weight-based pricing applied (checkbox ON)")







# import frappe

# def po_calculation_by_weight(doc, method):

#     # 🔒 Run only when checkbox ON
#     if not doc.custom_calculate_based_on_weight:
#         return

#     total_doc_amount = 0

#     for item in doc.items:
#         try:
#             base_amount = float(item.custom_custom_rate or 0)
#             weight_per_unit = float(item.weight_per_unit or 0)
#             qty = float(item.qty or 0)
#         except Exception:
#             continue

#         # Skip if no base amount
#         if base_amount <= 0:
#             item.amount = 0
#             continue

#         # 🧮 RATE calculation
#         if weight_per_unit > 0:
#             final_rate = round(base_amount * weight_per_unit, 2)
#         else:
#             final_rate = round(base_amount, 2)

#         # 🧮 AMOUNT calculation
#         final_amount = round(final_rate * qty, 2)

#         # 🔥 UPDATE ALL ERP FIELDS (as you requested)
#         item.rate = final_rate
#         item.net_rate = final_rate
#         item.base_rate = final_rate
#         item.base_net_rate = final_rate

#         item.amount = final_amount
#         item.net_amount = final_amount
#         item.base_amount = final_amount
#         item.base_net_amount = final_amount
#         item.taxable_value = final_amount

#         total_doc_amount += final_amount

#     # ✅ Correct total for whole document
#     doc.total = total_doc_amount
#     doc.net_total = total_doc_amount
#     doc.base_total = total_doc_amount
#     doc.base_net_total = total_doc_amount

#     frappe.msgprint("✅ Custom weight pricing applied successfully")





import frappe

def po_calculation_by_weight(doc, method):

    # 🔒 Run only when checkbox ON
    if not doc.custom_calculate_based_on_weight:
        return

    total_doc_amount = 0

    for item in doc.items:
        try:
            custom_rate = float(item.custom_custom_rate or 0)
            weight_per_unit = float(item.weight_per_unit or 0)
            qty = float(item.qty or 0)
            normal_rate = float(item.rate or 0)
        except Exception:
            continue

        # ==============================
        # 🟢 CASE 1 → Custom rate entered
        # ==============================
        if custom_rate > 0:

            if weight_per_unit > 0:
                final_rate = round(custom_rate * weight_per_unit, 2)
            else:
                final_rate = round(custom_rate, 2)

            final_amount = round(final_rate * qty, 2)

            # 🔥 Update all fields
            item.rate = final_rate
            item.net_rate = final_rate
            item.base_rate = final_rate
            item.base_net_rate = final_rate

            item.amount = final_amount
            item.net_amount = final_amount
            item.base_amount = final_amount
            item.base_net_amount = final_amount
            item.taxable_value = final_amount

            total_doc_amount += final_amount

        # ==============================
        # 🟡 CASE 2 → Custom rate = 0
        # 👉 Use normal ERPNext behaviour
        # ==============================
        else:
            normal_amount = round(normal_rate * qty, 2)
            total_doc_amount += normal_amount

    # ✅ Update doc totals
    doc.total = total_doc_amount
    doc.net_total = total_doc_amount
    doc.base_total = total_doc_amount
    doc.base_net_total = total_doc_amount














