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








