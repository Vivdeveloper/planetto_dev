from india_compliance.gst_india.overrides.transaction import ItemGSTDetails

class CustomItemGSTDetails(ItemGSTDetails):
    def validate_item_gst_details(self):
        """
        Skip GST validation ONLY when:
        - Document is Purchase Order
        - AND custom_calculate_based_on_weight == 1

        Otherwise, use standard GST validation.
        """

        doc = getattr(self, "doc", None)

        try:
            # If this is NOT a Purchase Order, enforce GST validation
            if not doc or doc.doctype != "Purchase Order":
                return super().validate_item_gst_details()

            # If checkbox is NOT enabled, enforce GST validation
            if not getattr(doc, "custom_calculate_based_on_weight", 0):
                return super().validate_item_gst_details()

            # ✅ Safe skip for weight-based Purchase Orders
            return

        except Exception:
            # 🔒 Failsafe: if anything goes wrong, enforce GST
            return super().validate_item_gst_details()
