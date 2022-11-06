# Copyright (c) 2013, Mohammad Ali and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import date_diff


def execute(filters):
    columns, data = [], []
    columns = [
        {
		"label": _("Voucher No."),
				"fieldname": "voucher_no",
				"fieldtype": "Link",
				"options": "Payment Entry",
				"width": 180
	},
        {
        "label": _("Cheque Received Date"),
     			"fieldname": "cheque_rec_date",
     			"fieldtype": "Date",
     			"width": 150
    },
		{
        "label": _("Cheque Number"),
     			"fieldname": "ref_number",
     			"fieldtype": "Data",
    },
        {
        "label": _("Amount Received"),
     			"fieldname": "amount_received",
     			"fieldtype": "Currency",
     			"width": 150
    },
        {
        "label": _("Cheque Received Days"),
     			"fieldname": "cheq_rec_days",
     			"fieldtype": "Data",
     			"width": 150
    },
        {
        "label": _("Sales Invoice Date"),
     			"fieldname": "si_date",
     			"fieldtype": "Date",
     			"width": 150
    },
        {
        "label": _("Sales Invoice"),
     			"fieldname": "sales_invoice",
     			"fieldtype": "Link",
     			"options": "Sales Invoice",
     			"width": 150
    },
        {
        "label": _("Total Bill Amount"),
     			"fieldname": "total_bill_amount",
     			"fieldtype": "Currency",
     			"width": 150
	},
        {
		"label": _("Total Outstanding"),
				"fieldname": "total_outstanding",
				"fieldtype": "Currency",
				"width": 150
	},
        {
        "label": _("Status"),
     			"fieldname": "status",
     			"fieldtype": "Data",
     			"width": 150
    },
        {
        "label": _("Total Ageing"),
     			"fieldname": "total_ageing",
     			"fieldtype": "Data",
     			"width": 150
    },
        {
        "label": _("Difference"),
     			"fieldname": "difference",
     			"fieldtype": "Currency",
     			"width": 150
    },
        {
        "label": _("Cheque Status"),
     			"fieldname": "cheque_status",
     			"fieldtype": "Data",
     			"width": 150
    },
    ]

    data = get_data(filters)
    return columns, data


def get_data(filters=None):
	conditions = []
	data = []
	
	if filters.get('party'):
		conditions.append("tpe.party = '{}' ".format(filters.get('party')))
	
	if filters.get('payment_entry'):
		conditions.append("tpe.name = '{}' ".format(filters.get('payment_entry')))

	if filters.get("voucher_date"):
		if date_diff(filters.get("voucher_date")[1], filters.get("voucher_date")[0]) < 0:
			frappe.throw('To Date must be greater than from date')
		conditions.append("tpe.reference_date between '{}' and '{}' ".format(
		    filters.get("voucher_date")[0], filters.get("voucher_date")[1]))

	if filters.get('cheque_no'):
		conditions.append("tpe.reference_no like '%%{}%%' ".format(
		    filters.get('cheque_no')))


	where_clause = ""
	if len(conditions) > 0:
		where_clause = "and ".join(conditions)
		where_clause = "and "+where_clause

	pe_list = frappe.db.sql("""select
			tpe.name,
			tpe.reference_no,
			tpe.reference_date,
			tpe.paid_amount,
			(
			select
				tsi.posting_date
			from
				`tabSales Invoice` tsi
			where
				tsi.name = tper.reference_name) as 'si_date',
			(
			select
				tsi.status
			from
				`tabSales Invoice` tsi
			where
				tsi.name = tper.reference_name) as 'ref_status',
			tper.reference_name,
			tper.total_amount,
			tper.outstanding_amount,
			tpe.workflow_state as cheque_status
		from
			`tabPayment Entry` tpe
		inner join `tabPayment Entry Reference` tper
		on tpe.name = tper.parent
		where tper.reference_doctype = "Sales Invoice"
		and tpe.reference_no is not NULL and tpe.reference_date is not Null
		and tpe.docstatus = 1
		-- and tpe.workflow_state in ('Cheque Cleared')
		{}
		""".format(where_clause), as_dict=True)
	pe_id =  ""
	for pe in pe_list:
		if pe.reference_date is None:
			a=0
		cheque_received_days = (pe.reference_date - pe.si_date).days
		ageing = (frappe.utils.now_datetime().date() - pe.si_date).days
		diff_amount = pe.outstanding_amount - pe.paid_amount
		if pe_id != pe.name:
			data.append({
						"voucher_no": pe.name,
						"cheque_rec_date": pe.reference_date,
						"ref_number": pe.reference_no,
						"amount_received": pe.paid_amount,
						"cheq_rec_days": cheque_received_days,
						"si_date": pe.si_date,
						"sales_invoice": pe.reference_name,
						"total_bill_amount": pe.total_amount,
						"total_outstanding": pe.outstanding_amount,
						"status": pe.ref_status,
						"total_ageing": str(ageing) + " Days",
						"difference": diff_amount,
						"cheque_status": pe.cheque_status,
					})
			pe_id = pe.name

		else:
			data.append({
					"si_date": pe.si_date,
					"sales_invoice": pe.reference_name,
					"total_bill_amount": pe.total_amount,
					"total_outstanding": pe.outstanding_amount,
					"status": pe.ref_status,
					"total_ageing": str(ageing) + " Days",
					"difference": diff_amount,
					"cheque_status": pe.cheque_status,
                })
			pe_id = pe.name
	return data
