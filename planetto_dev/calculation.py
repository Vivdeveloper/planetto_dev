
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






import frappe

def po_calculation_by_weight(doc, method):
    # Apply ONLY when checkbox is ticked
    if not doc.custom_calculate_based_on_weight:
        return

    for item in doc.items:
        # Safety: if rate missing, skip
        if not item.rate:
            item.amount = 0
            continue

        # STRICT weight-based calculation
        # If total_weight is 0 or None → amount becomes 0
        weight = float(item.total_weight or 0)
        rate = float(item.rate)

        item.amount = weight * rate   
    
    # Proof popup
    frappe.msgprint("✅ Strict weight-based calculation applied")



















