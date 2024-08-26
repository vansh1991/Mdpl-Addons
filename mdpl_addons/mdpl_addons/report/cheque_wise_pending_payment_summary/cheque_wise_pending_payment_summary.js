// Copyright (c) 2022, Mohammad Ali and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cheque Wise Pending Payment Summary"] = {
	"filters": [
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd":1,
            "default":frappe.datetime.add_months(frappe.datetime.get_today(), -2),
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd":1,
            "default": frappe.datetime.get_today(),
        },
		{
			"fieldname":"customer",
			"fieldtype":"MultiSelectList",
			"label":"Customer",
			"options":"Customer",
			"get_data": function(txt) {
				return frappe.db.get_link_options("Customer", txt);
			},
		},
		{
			'label': 'Check Payment Entry',
			'fieldname': 'payment_entry',
			'fieldtype': 'Select',
			'options': ' \nYes\nNo'
		}
		
	]
};
