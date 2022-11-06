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
			"width": 200
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
        "label": _("POE"),
     			"fieldname": "poe",
     			"fieldtype": "Data",
     			"width": 150
    },
        {
        "label": _("Inward Invoice"),
     			"fieldname": "inward_invoice",
     			"fieldtype": "Data",
     			"width": 150
    },
        {
        "label": _("Inward Delivery Date"),
     			"fieldname": "inward_delivery_date",
     			"fieldtype": "Date",
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

	if filters.get('bill_no'):
		conditions.append("tpi.bill_no = '{}' ".format(filters.get('bill_no')))

	if filters.get("bill_date"):
		if date_diff(filters.get("bill_date")[1], filters.get("bill_date")[0]) < 0:
			frappe.throw('To Date must be greater than from date')
		conditions.append("tpi.posting_date between '{}' and '{}' ".format(
		    filters.get("bill_date")[0], filters.get("bill_date")[1]))

	if filters.get('item_code'):
		conditions.append("tpii.item_code = '{}' ".format(filters.get('item_code')))

	if filters.get('serial_no'):
		conditions.append("tpii.serial_no like '%%{}%%' ".format(filters.get('serial_no')))

	where_clause = ""
	if len(conditions) > 0:
		where_clause = "and ".join(conditions)
		where_clause = "and "+where_clause

	pi_list = frappe.db.sql("""select
		tpii.item_code,
		tpii.serial_no,
		tpi.bill_no ,
		tpi.posting_date as bill_date ,
		tpii.item_group
		from
		`tabPurchase Invoice` tpi
		left join `tabPurchase Invoice Item` tpii on
		tpi.name = tpii.parent
		where
		tpi.docstatus and
		(select has_serial_no from tabItem ti where name = tpii.item_code) = 1
		{}
		""".format(where_clause), as_dict=True)

	for pi in pi_list:
		serial_nos = ""
		serial_nos = pi.serial_no
		#frappe.log_error(serial_nos)
		serial_nos = serial_nos.split('\n')

		poe = "Haryana"
		if serial_nos:
			if len(serial_nos) > 0:
				for serial in serial_nos:
					imei = ""
					serial_no = ""
					if pi.item_group and pi.item_group.lower() == "iphone".lower():
						imei = serial
					elif pi.item_group and pi.item_group.lower() in ['ipad', 'apple watch', 'airpods']:
						serial_no = serial
					if filters.get('serial_no'):
						if filters.get('serial_no') == serial:
							data.append({
								"item_code": pi.item_code,
								"imei_1": imei,
								"serial_no": serial_no,
								"poe": poe,
								"inward_invoice": pi.bill_no,
								"inward_delivery_date": pi.bill_date,
							})
					else:
						data.append({
							"item_code": pi.item_code,
							"imei_1": imei,
							"serial_no": serial_no,
							"poe": poe,
							"inward_invoice": pi.bill_no,
							"inward_delivery_date": pi.bill_date,
						})
						
			else:
				data.append({
					"item_code": pi.item_code,
					"poe": poe,
					"inward_invoice": pi.bill_no,
					"inward_delivery_date": pi.bill_date,
				})
		

	return data
