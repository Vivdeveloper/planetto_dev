def calculate_weight(doc, method=None):
    category = doc.custom_category or ""
    weight = 0

    if category == "FLAT BAR":
        length = doc.custom_length or 0
        width = doc.custom_width or 0
        height = doc.custom_height_ or 0

        weight = length * width * height * 0.00000785

    elif category == "ROUND BAR":
        dia = doc.custom_dia or 0
        width = doc.custom_width or 0
        height = doc.custom_height_ or 0

        weight = (dia * dia * height * 1) / 162300

    elif category == "ACTUAL DIE WT":
        length = doc.custom_length or 0
        width = doc.custom_width or 0
        height = doc.custom_height_ or 0

        weight = length * width * height * 0.00000785 * 0.5

    # Set calculated weight
    doc.weight_per_unit = round(weight, 2)

    # ✅ Auto set UOM when weight is calculated
    if weight > 0:
        doc.weight_uom = "Kg"