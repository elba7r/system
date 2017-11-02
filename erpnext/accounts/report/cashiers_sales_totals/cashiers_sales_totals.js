// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors and contributors
// For license information, please see license.txt

frappe.query_reports["Cashiers Sales Totals"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": sys_defaults.year_start_date,
		},
		{
			"fieldname":"posting_time",
			"label": __("From Time"),
			"fieldtype": "Data",
			"width": "80",
			"default": "00:00:00"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"posting_time",
			"label": __("To Time"),
			"fieldtype": "Data",
			"width": "80",
			"default": "00:00:00"
		},
		{
			"fieldname": "territory",
			"label": __("Territory"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Territory"
		},
	]
}
