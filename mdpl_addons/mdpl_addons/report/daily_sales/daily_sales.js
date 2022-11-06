// Copyright (c) 2016, Mohammad Ali and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Sales"] = {
	"filters": [
		{
			'label': 'Outward Invoice',
			'fieldname': 'sales_invoice',
			'fieldtype': 'Link',
			'options': 'Sales Invoice'
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
			'label': 'Outward Delivery Date',
			'fieldname': 'delivery_date',
			'fieldtype': 'DateRange',
			'default': [frappe.datetime.add_months(frappe.datetime.nowdate(),-1), frappe.datetime.nowdate()]
		},
	]
};
