# Copyright (c) 2013, Mohammad Ali and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import date_diff


def execute(filters):
    columns, data = [], []
    columns = [{
			"label": _("MPN"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"label": _("IMEI 1"),
			"fieldname": "imei_1",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("IMEI 2"),
			"fieldname": "imei_2",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Serial No"),
			"fieldname": "serial_no",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Outward Invoice"),
			"fieldname": "outward_invoice",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 150
		},
		{
			"label": _("Outward Delivery Date"),
			"fieldname": "outward_delivery_date",
			"fieldtype": "Date",
			"width": 150
		},
        {
			"label": _("POS ID"),
			"fieldname": "outward_sold",
			"fieldtype": "Data",
			"width": 150
    	},
    ]

    data = get_data(filters)
    return columns, data


def get_data(filters=None):
	conditions = []
	data = []
	# if filters.customer:
	#     q_filters['customer'] = filters.customer

	if filters.get('sales_invoice'):
		conditions.append("tsi.name = '{}' ".format(filters.get('sales_invoice')))
	
	if filters.get("delivery_date"):
		if date_diff(filters.get("delivery_date")[1], filters.get("delivery_date")[0]) < 0:
			frappe.throw('To Date must be greater than from date')
		conditions.append("tsi.posting_date between '{}' and '{}' ".format(
		    filters.get("delivery_date")[0], filters.get("delivery_date")[1]))

	if filters.get('item_code'):
		conditions.append("tsii.item_code = '{}' ".format(filters.get('item_code')))

	if filters.get('serial_no'):
		conditions.append("tsii.serial_no like '%%{}%%' ".format(filters.get('serial_no')))

	where_clause = ""
	if len(conditions) > 0:
		where_clause = "and ".join(conditions)
		where_clause = "and "+where_clause
	
	

	si_list = frappe.db.sql("""select
		tsii.item_code,
		tsii.serial_no,
		tsi.name,
		tsi.posting_date,
		tsii.item_group,
		( select apple_id from tabCustomer tc where tc.name = tsi.customer limit 1 ) apple_id
		from
		`tabSales Invoice` tsi
		left join `tabSales Invoice Item` tsii on
		tsi.name = tsii.parent
		where
		tsi.docstatus = 1 and
		(select has_serial_no from tabItem ti where name = tsii.item_code) = 1
		{}
		""".format(where_clause), as_dict=True)

	for si in si_list:
		serial_nos = ""
		serial_nos = si.serial_no
		serial_nos = serial_nos.split('\n')
		if len(serial_nos) > 0:
			for serial in serial_nos:
				imei = ""
				serial_no = ""
				if si.item_group and si.item_group.lower() == "iphone".lower():
					imei = serial
				elif si.item_group and si.item_group.lower() in ['ipad', 'apple watch', 'airpods']:
					serial_no = serial
				
				if filters.get('serial_no'):
					if filters.get('serial_no') == serial:
						data.append({
							"item_code": si.item_code,
							"imei_1": imei,
							"serial_no": serial_no,
							"outward_invoice": si.name,
							"outward_delivery_date": si.posting_date,
							"outward_sold": si.apple_id
						})
				else:
					data.append({
						"item_code": si.item_code,
						"imei_1": imei,
						"serial_no": serial_no,
						"outward_invoice": si.name,
						"outward_delivery_date": si.posting_date,
						"outward_sold": si.apple_id
					})
		else:
			data.append({
				"item_code": si.item_code,
				"outward_invoice": si.name,
				"outward_delivery_date": si.posting_date,
				"outward_sold": si.apple_id
			})


	return data
