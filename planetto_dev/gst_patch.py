# import frappe

# def apply_gst_patch():
#     print("GST PATCH ACTIVE")
#     """
#     Version-independent GST monkey patch.
#     Safely skips item GST validation ONLY for:
#     - Purchase Order
#     - custom_calculate_based_on_weight == 1
#     """

#     try:
#         from india_compliance.gst_india.overrides import transaction
#     except Exception:
#         # India Compliance not installed
#         return

#     cls = getattr(transaction, "ItemGSTDetails", None)
#     if not cls:
#         return

#     # Find a validation method dynamically
#     method_name = None
#     for name in [
#         "validate_item_gst_details",
#         "validate_item_tax_details",
#         "validate_item_tax_breakup",
#     ]:
#         if hasattr(cls, name):
#             method_name = name
#             break

#     # If no known method found, do nothing
#     if not method_name:
#         return

#     original_method = getattr(cls, method_name)

#     def patched(self, *args, **kwargs):
#         try:
#             doc = getattr(self, "doc", None)

#             # Only skip for Purchase Order + flag ON
#             if (
#                 doc
#                 and getattr(doc, "doctype", None) == "Purchase Order"
#                 and getattr(doc, "custom_calculate_based_on_weight", 0)
#             ):
#                 return  # ✅ Skip GST validation
#         except Exception:
#             pass

#         # Fallback to original behavior
#         return original_method(self, *args, **kwargs)

#     # 🔥 Patch at runtime
#     setattr(cls, method_name, patched)

