// Copyright (c) 2022, Mohammad Ali and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cheque Wise Cleared Payment Summary"] = {
	"filters": [
		{
			'label': 'Party Name',
			'fieldname': 'party',
			'fieldtype': 'Link',
			'options': 'Customer'
		},
		{
			'label': 'Voucher No',
			'fieldname': 'payment_entry',
			'fieldtype': 'Link',
			'options': 'Payment Entry'
		},
		{
			'label': 'Voucher Date',
			'fieldname': 'voucher_date',
			'fieldtype': 'DateRange',
			'default': [frappe.datetime.add_months(frappe.datetime.nowdate(), -1), frappe.datetime.nowdate()]
		},
		{
			'label': 'Cheque No',
			'fieldname': 'cheque_no',
			'fieldtype': 'Data'
		},
		

	]
};
