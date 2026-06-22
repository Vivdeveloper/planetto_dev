// Copyright (c) 2026, sanket and contributors
// For license information, please see license.txt

const VIEW_MONTHLY = "Monthly Order Booking";
const VIEW_YEARLY_MONTHLY = "Yearly Monthly Summary";
const VIEW_CUSTOMER = "Customer Wise";
const VIEW_CATEGORY = "Category Wise";
const VIEW_SEGMENT = "Segment Wise";

const MONTH_ALLOWED_VIEWS = [
	VIEW_MONTHLY,
	VIEW_CUSTOMER,
	VIEW_CATEGORY,
	VIEW_SEGMENT,
];

frappe.query_reports["Order Booking"] = {
	filters: [
		{
			fieldname: "view_type",
			label: __("Report View"),
			fieldtype: "Select",
			options: [
				VIEW_YEARLY_MONTHLY,
				VIEW_MONTHLY,
				VIEW_CUSTOMER,
				VIEW_CATEGORY,
				VIEW_SEGMENT,
			],
			default: VIEW_YEARLY_MONTHLY,
			reqd: 1,
			on_change: () => toggle_dependent_filters(),
		},
		{
			fieldname: "year",
			label: __("Year"),
			fieldtype: "Select",
			options: getYears(),
			default: new Date().getFullYear(),
			on_change: () => toggle_dependent_filters(),
		},
		{
			fieldname: "month",
			label: __("Month"),
			fieldtype: "Select",
			options: getMonths(),
			default: getDefaultMonth(),
			depends_on: `eval:doc.year && ${JSON.stringify(MONTH_ALLOWED_VIEWS)}.includes(doc.view_type)`,
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "category",
			label: __("Category"),
			fieldtype: "Link",
			options: "Category",
		},
		{
			fieldname: "segment",
			label: __("Segment"),
			fieldtype: "Link",
			options: "Industries",
		},
	],
	onload(report) {
		toggle_dependent_filters(report);
	},
};

function toggle_dependent_filters(report = frappe.query_report) {
	const view_type = report.get_filter_value("view_type");
	const year = report.get_filter_value("year");
	const year_filter = report.get_filter("year");
	const month_filter = report.get_filter("month");

	const year_required_views = [VIEW_MONTHLY, VIEW_YEARLY_MONTHLY];
	year_filter.df.reqd = year_required_views.includes(view_type);
	year_filter.refresh();

	const show_month = year && MONTH_ALLOWED_VIEWS.includes(view_type);
	if (!show_month) {
		month_filter.set_value("");
	}
	month_filter.toggle(show_month);
}

function getYears() {
	const currentYear = new Date().getFullYear();
	const years = [""];
	for (let year = currentYear; year >= currentYear - 10; year--) {
		years.push(year);
	}
	return years;
}

function getMonths() {
	return [
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
	];
}

function getDefaultMonth() {
	return getMonths()[new Date().getMonth() + 1];
}
