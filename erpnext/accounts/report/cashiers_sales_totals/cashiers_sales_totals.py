# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate, cint, cstr, get_time, to_timedelta

def execute(filters=None):
	if not filters: filters = {}

	validate_filters(filters)

	columns = get_columns()
	
	iwb_map = get_item_warehouse_map(filters)

	data = []
	for (territory) in sorted(iwb_map):
		qty_dict = iwb_map[(territory)]
		data.append([
			qty_dict.territory,
			qty_dict.total
		])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Territory")+":Data:300",
		_("Total")+":Float:100"
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if not filters.get("from_date"):
		frappe.throw(_("'From Date' is required"))
	
	if filters.get("from_time"):
    		conditions += " and posting_time = '%s'" % frappe.db.escape(filters["from_time"])

	if filters.get("to_date"):
		conditions += " and posting_date <= '%s'" % frappe.db.escape(filters["to_date"])
	else:
		frappe.throw(_("'To Date' is required"))

	if filters.get("to_time"):
    		conditions += " and posting_time = '%s'" % frappe.db.escape(filters["to_time"])
	
	if filters.get("territory"):
		    conditions += " and territory = '%s'" % frappe.db.escape(filters.get("territory"), percent=False)
	
	


	return conditions

def get_sales_invoice_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select territory, grand_total, posting_date, posting_time
		from `tabSales Invoice` 
		where docstatus < 2 %s order by posting_date, posting_time, name""" %
		conditions, as_dict=1)

def get_item_warehouse_map(filters):
	iwb_map = {}
	from_time = to_timedelta(filters["posting_time"])
	from_date = getdate(filters["from_date"])
	to_date = getdate(filters["to_date"])
	to_time = to_timedelta(filters["posting_time"])
	
	
	

	sie = get_sales_invoice_entries(filters)

	for d in sie:
		key = (d.territory)
		if key not in iwb_map:
			iwb_map[key] = frappe._dict({
				"total": 0.0,
				"territory": d.territory
			})

		qty_dict = iwb_map[(d.territory)]

		if (d.posting_date == from_date and d.posting_time >= from_time) or (d.posting_date > from_date and d.posting_date < to_date) or (d.posting_date == to_date and d.posting_time <= to_time):
    	    
		    qty_dict.territory = d.territory
		    qty_dict.total += d.grand_total
		
      

	return iwb_map



def validate_filters(filters):
	if not (filters.get("territory")):
		sie_count = flt(frappe.db.sql("""select count(name) from `tabSales Invoice`""")[0][0])
		if sie_count > 500000:
			frappe.throw(_("Please set filter based on Item or Warehouse"))
