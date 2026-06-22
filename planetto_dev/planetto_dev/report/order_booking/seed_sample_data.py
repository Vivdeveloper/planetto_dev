"""Seed Order Booking sample data for report verification (2022-2025)."""

from datetime import date

import frappe

SAMPLE_DATA = [
	# 2022
	{"year": 2022, "month": 1, "customer": "CUST0009", "amount": 150000, "industries": "4W", "category": "PARTS", "po_no": "PO-2022-01", "description": "Sample 2022 Jan - Parts order"},
	{"year": 2022, "month": 3, "customer": "CUST0013", "amount": 275000, "industries": "2W", "category": "PROTO TOOLING", "po_no": "PO-2022-03", "description": "Sample 2022 Mar - Proto tooling"},
	{"year": 2022, "month": 6, "customer": "CUST0060", "amount": 420000, "industries": "4W", "category": "DIE MANUFACTURING", "po_no": "PO-2022-06", "description": "Sample 2022 Jun - Die manufacturing"},
	{"year": 2022, "month": 9, "customer": "CUST0086", "amount": 98000, "industries": "STAMPING", "category": "SERVICES", "po_no": "PO-2022-09", "description": "Sample 2022 Sep - Services"},
	{"year": 2022, "month": 12, "customer": "CUST0092", "amount": 310500, "industries": "4W", "category": "PARTS", "po_no": "PO-2022-12", "description": "Sample 2022 Dec - Parts order"},
	# 2023
	{"year": 2023, "month": 2, "customer": "CUST0009", "amount": 185000, "industries": "4W", "category": "PARTS", "po_no": "PO-2023-02", "description": "Sample 2023 Feb - Parts order"},
	{"year": 2023, "month": 4, "customer": "CUST0088", "amount": 540000, "industries": "4W", "category": "DIES & PANEL CHECKER", "po_no": "PO-2023-04", "description": "Sample 2023 Apr - Dies & panel checker"},
	{"year": 2023, "month": 5, "customer": "CUST0091", "amount": 225000, "industries": "2W", "category": "SPARE PARTS", "po_no": "PO-2023-05", "description": "Sample 2023 May - Spare parts"},
	{"year": 2023, "month": 8, "customer": "CUST0093", "amount": 167800, "industries": "STAMPING", "category": "SERVICES", "po_no": "PO-2023-08", "description": "Sample 2023 Aug - Services"},
	{"year": 2023, "month": 11, "customer": "CUST0013", "amount": 890000, "industries": "4W", "category": "PROTO TOOLING", "po_no": "PO-2023-11", "description": "Sample 2023 Nov - Proto tooling"},
	# 2024
	{"year": 2024, "month": 1, "customer": "CUST0060", "amount": 125000, "industries": "4W", "category": "PARTS", "po_no": "PO-2024-01", "description": "Sample 2024 Jan - Parts order"},
	{"year": 2024, "month": 3, "customer": "CUST0086", "amount": 456000, "industries": "2W", "category": "DEVELOPMENT COST", "po_no": "PO-2024-03", "description": "Sample 2024 Mar - Development cost"},
	{"year": 2024, "month": 5, "customer": "CUST0009", "amount": 712000, "industries": "4W", "category": "DIES & PANEL CHECKER", "po_no": "PO-2024-05", "description": "Sample 2024 May - Dies & panel checker"},
	{"year": 2024, "month": 7, "customer": "CUST0094", "amount": 198500, "industries": "STAMPING", "category": "PROTO PARTS", "po_no": "PO-2024-07", "description": "Sample 2024 Jul - Proto parts"},
	{"year": 2024, "month": 10, "customer": "CUST0092", "amount": 335000, "industries": "4W", "category": "PARTS", "po_no": "PO-2024-10", "description": "Sample 2024 Oct - Parts order"},
	# 2025 — all 12 months for cross-verification
	{"year": 2025, "month": 1, "customer": "CUST0092", "amount": 210000, "industries": "4W", "category": "PARTS", "po_no": "PO-2025-01", "description": "Sample 2025 Jan - Parts order"},
	{"year": 2025, "month": 2, "customer": "CUST0013", "amount": 245000, "industries": "4W", "category": "PARTS", "po_no": "PO-2025-02", "description": "Sample 2025 Feb - Parts order"},
	{"year": 2025, "month": 3, "customer": "CUST0086", "amount": 312000, "industries": "2W", "category": "DEVELOPMENT COST", "po_no": "PO-2025-03", "description": "Sample 2025 Mar - Development cost"},
	{"year": 2025, "month": 4, "customer": "CUST0088", "amount": 620000, "industries": "4W", "category": "DIE MANUFACTURING", "po_no": "PO-2025-04", "description": "Sample 2025 Apr - Die manufacturing"},
	{"year": 2025, "month": 5, "customer": "CUST0094", "amount": 278500, "industries": "STAMPING", "category": "SERVICES", "po_no": "PO-2025-05", "description": "Sample 2025 May - Services"},
	{"year": 2025, "month": 6, "customer": "CUST0009", "amount": 388000, "industries": "2W", "category": "SERVICES", "po_no": "PO-2025-06", "description": "Sample 2025 Jun - Services"},
	{"year": 2025, "month": 7, "customer": "CUST0060", "amount": 415000, "industries": "4W", "category": "PROTO TOOLING", "po_no": "PO-2025-07", "description": "Sample 2025 Jul - Proto tooling"},
	{"year": 2025, "month": 8, "customer": "CUST0093", "amount": 192000, "industries": "STAMPING", "category": "SPARE PARTS", "po_no": "PO-2025-08", "description": "Sample 2025 Aug - Spare parts"},
	{"year": 2025, "month": 9, "customer": "CUST0091", "amount": 175000, "industries": "STAMPING", "category": "SPARE PARTS", "po_no": "PO-2025-09", "description": "Sample 2025 Sep - Spare parts"},
	{"year": 2025, "month": 10, "customer": "CUST0009", "amount": 356000, "industries": "4W", "category": "DIES & PANEL CHECKER", "po_no": "PO-2025-10", "description": "Sample 2025 Oct - Dies & panel checker"},
	{"year": 2025, "month": 11, "customer": "CUST0013", "amount": 289000, "industries": "4W", "category": "PARTS", "po_no": "PO-2025-11", "description": "Sample 2025 Nov - Parts order"},
	{"year": 2025, "month": 12, "customer": "CUST0060", "amount": 502000, "industries": "4W", "category": "PROTO TOOLING", "po_no": "PO-2025-12", "description": "Sample 2025 Dec - Proto tooling"},
]


def seed_order_booking_sample_data():
	created = []
	skipped = []

	for row in SAMPLE_DATA:
		po_no = row["po_no"]
		if frappe.db.exists("Order Booking", {"po_no": po_no}):
			skipped.append(po_no)
			continue

		customer_name = frappe.db.get_value("Customer", row["customer"], "customer_name")
		doc = frappe.new_doc("Order Booking")
		doc.posting_date = date(row["year"], row["month"], 15)
		doc.customer = row["customer"]
		doc.customer_name = customer_name
		doc.amount = row["amount"]
		doc.industries = row["industries"]
		doc.category = row["category"]
		doc.po_no = po_no
		doc.description = row["description"]
		doc.insert()
		doc.submit()
		created.append(doc.name)

	frappe.db.commit()
	return {"created": created, "skipped": skipped}
