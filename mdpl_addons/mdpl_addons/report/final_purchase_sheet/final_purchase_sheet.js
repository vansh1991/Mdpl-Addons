// Copyright (c) 2016, Mohammad Ali and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Final Purchase Sheet"] = {
	"filters": [
		{
			'label': 'Inward Invoice',
			'fieldname': 'bill_no',
			'fieldtype': 'Data'
		},
		{
			'label': 'Item Code',
			'fieldname': 'item_code',
			'fieldtype': 'Link',
			'options': 'Item'
		},
		{
			'label': 'Serial No',
			'fieldname': 'serial_no',
			'fieldtype': 'Link',
			'options': 'Serial No'
		},
		{
			'label': 'Inward Invoice Date',
			'fieldname': 'bill_date',
			'fieldtype': 'DateRange',
			'default': [frappe.datetime.add_months(frappe.datetime.nowdate(), -1), frappe.datetime.nowdate()]
		},
	]
};
