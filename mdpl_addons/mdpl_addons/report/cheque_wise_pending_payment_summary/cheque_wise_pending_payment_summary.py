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
        		"label": _("Customer"),
     			"fieldname": "customer",
     			"fieldtype": "Link",
     			"options": "CUstomer",
     			"width": 180
    	},
        {
        		"label": _("Sales Invoice"),
     			"fieldname": "sales_invoice",
     			"fieldtype": "Link",
     			"options": "Sales Invoice",
     			"width": 180
    	},
        {
        		"label": _("Sales Invoice Date"),
     			"fieldname": "si_date",
     			"fieldtype": "Date",
     			"width": 150
    	},
        {
        		"label": _("Total Bill Amount"),
     			"fieldname": "total_bill_amount",
     			"fieldtype": "Currency",
     			"width": 150
    	},
		{
        		"label": _("Allocated Amount"),
     			"fieldname": "allocated_amount",
     			"fieldtype": "Currency",
     			"width": 150
    	},
        {
        		"label": _("Total Outstanding"),
     			"fieldname": "total_outstanding",
     			"fieldtype": "Float",
     			"width": 150
    	},
		{
        		"label": _("Payment Entry"),
     			"fieldname": "payment_entry",
     			"fieldtype": "Link",
     			"options": "Payment Entry",
     			"width": 180
    	},
		{
        		"label": _("Cheque Amount"),
     			"fieldname": "paid_amount",
     			"fieldtype": "Currency",
     			"width": 150
    	},
		
		{
        		"label": _("Outstanding Days"),
     			"fieldname": "outstanding_days",
     			"fieldtype": "Data",
     			"width": 150
    	},
		{
        		"label": _("Cheque Days"),
     			"fieldname": "cheque_days",
     			"fieldtype": "Data",
     			"width": 150
    	},
		{
        		"label": _("Cheque Ref. No."),
     			"fieldname": "ref_no",
     			"fieldtype": "Data",
     			"width": 150
    	},
		{
        		"label": _("Cheque Ref. Date"),
     			"fieldname": "ref_date",
     			"fieldtype": "Date",
     			"width": 150
    	},
        {
        		"label": _("PE Status"),
     			"fieldname": "status",
     			"fieldtype": "Data",
     			"width": 150
    	}
	]

    data = get_data(filters)
    return columns, data



def get_data(filters=None):
	conditions = ""
	data = []

	if filters.from_date and filters.to_date:
		conditions+=f" and tsi.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}' "

	get_customer_list=[]
	if filters.get("customer"):
		for d in filters.get("customer"):
			frappe.log_error("customer",d)
			get_customer_list.append({
				"customer":d
			})


	else:
		get_customer_list=frappe.db.sql("Select customer from `tabSales Invoice` where outstanding_amount > 0 and status != 'Return' group by customer",as_dict=1)

	
	if get_customer_list:
		pe_list = []
		for cust in get_customer_list:
			pe_list_invoice=frappe.db.sql(f"""select
				tsi.customer as 'customer',
				tsi.posting_date as 'si_date',
				tsi.name as 'si_name',
				tsi.status as 'ref_status',
				tsi.rounded_total as 'total_amount',
				tsi.outstanding_amount as 'outstanding_amount'
				
				from
					`tabSales Invoice` as tsi where tsi.outstanding_amount > 0 and docstatus <=1 and tsi.status != 'Return' and tsi.customer='{cust['customer']}'
				{conditions}
				order by tsi.posting_date asc""",as_dict=True)
			pe_list.append(pe_list_invoice)

		# Count=len(get_customer_list)
		for pel in pe_list:
			# frappe.log_error("Pe",pe)
			customer_name=""
			outstanding=0.0
			ot_amount=0
			for pe in pel:
				if pe.si_name:
					frappe.log_error("hh",filters.get("payment_entry"))
					if filters.get("payment_entry") == None:

						get_all_payment_entry=frappe.db.get_all("Payment Entry Reference",filters={"reference_name":pe.si_name,"reference_doctype":"Sales Invoice"},fields=["parent","allocated_amount","outstanding_amount","total_amount"])
						if get_all_payment_entry:
							# frappe.log_error("get_all_payment_entry",get_all_payment_entry)
							
							for pe_e in get_all_payment_entry:
								outstanding_days=(frappe.utils.now_datetime().date() - pe.si_date).days
								#out_total=#float(pe.total_amount)-float(pe_e.allocated_amount)
								data.append({
									"customer":pe.customer,
									"sales_invoice": pe.si_name,
									"si_date": pe.si_date,
									"total_bill_amount": pe.total_amount,
									"allocated_amount":pe_e.allocated_amount or 0,
									"total_outstanding":pe.outstanding_amount,#out_total,
									"payment_entry":pe_e.parent,
									"paid_amount":frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"paid_amount") or 0,
									"outstanding_days":outstanding_days,
									"cheque_days":(frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"reference_date") -pe.si_date).days,
									"ref_no":frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"reference_no"),
									"ref_date":frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"reference_date"),
									"status": frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"workflow_state")
								})
								# ot_amount+= pe_e.outstanding_amount
						else:
							outstanding_days=(frappe.utils.now_datetime().date() - pe.si_date).days
							data.append({
									"customer":pe.customer,
									"sales_invoice": pe.si_name,
									"si_date": pe.si_date,
									"total_bill_amount": pe.total_amount,
									"allocated_amount": 0,
									"total_outstanding": pe.outstanding_amount or 0,
									"payment_entry":"",
									"paid_amount":0,
									"outstanding_days":(frappe.utils.now_datetime().date() - pe.si_date).days,
									"cheque_days":0,
									"ref_no":"",
									"ref_date":"",
									"status": ""
							})
							# ot_amount+=	pe.outstanding_amount
					elif filters.get("payment_entry") == "Yes":
						get_all_payment_entry=frappe.db.get_all("Payment Entry Reference",filters={"reference_name":pe.si_name,"reference_doctype":"Sales Invoice"},fields=["parent","allocated_amount","outstanding_amount","total_amount"])
						if get_all_payment_entry:
							# frappe.log_error("get_all_payment_entry",get_all_payment_entry)
							
							for pe_e in get_all_payment_entry:
								outstanding_days=(frappe.utils.now_datetime().date() - pe.si_date).days
								out_total=float(pe.total_amount)-float(pe_e.allocated_amount)
								data.append({
									"customer":pe.customer,
									"sales_invoice": pe.si_name,
									"si_date": pe.si_date,
									"total_bill_amount": pe.total_amount,
									"allocated_amount":pe_e.allocated_amount or 0,
									"total_outstanding":pe.outstanding_amount,#float(pe_e.total_amount)-float(pe_e.allocated_amount),
									"payment_entry":pe_e.parent,
									"paid_amount":frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"paid_amount") or 0,
									"outstanding_days":outstanding_days,
									"cheque_days":(frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"reference_date") -pe.si_date).days,
									"ref_no":frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"reference_no"),
									"ref_date":frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"reference_date"),
									"status": frappe.db.get_value("Payment Entry",{"name":pe_e.parent},"workflow_state")

								})
								# ot_amount+= pe_e.outstanding_amount
					elif filters.get("payment_entry") == "No":
						data.append({
									"customer":pe.customer,
									"sales_invoice": pe.si_name,
									"si_date": pe.si_date,
									"total_bill_amount": pe.total_amount,
									"allocated_amount": 0,
									"total_outstanding": pe.outstanding_amount or 0,
									"payment_entry":"",
									"paid_amount":0,
									"outstanding_days":(frappe.utils.now_datetime().date() - pe.si_date).days,
									"cheque_days":0,
									"ref_no":"",
									"ref_date":"",
									"status": ""

							})
						# ot_amount+=	pe.outstanding_amount
					customer_name=pe.customer
					outstanding+=pe.outstanding_amount#get_outstanding(pe.si_name,filters.get("payment_entry"))


			# frappe.msgprint(str(pe_list))
			if outstanding>0:
				data.append({
					"customer":customer_name,
					"total_outstanding":outstanding
				})
				data.append({"customer":"","total_outstanding":""})

		
		frappe.log_error("customerlist",get_customer_list)
		
	return data


def get_outstanding(bill_no,payment_entry):
	get_all_payment_entry=frappe.db.get_all("Payment Entry Reference",filters={"reference_name":bill_no,"reference_doctype":"Sales Invoice"},fields=["parent","allocated_amount","outstanding_amount","total_amount"])
	out_s=0
	if payment_entry == None:
		if get_all_payment_entry:
			for pe_e in get_all_payment_entry:
				out_s+=frappe.db.get_value("Sales Invoice",{"name":bill_no},"outstanding_amount")#float(pe_e.total_amount)-float(pe_e.allocated_amount)
		else:
			out_s+=frappe.db.get_value("Sales Invoice",{"name":bill_no},"outstanding_amount")
	elif payment_entry == "Yes":
		if get_all_payment_entry:
			for pe_e in get_all_payment_entry:
				out_s+=frappe.db.get_value("Sales Invoice",{"name":bill_no},"outstanding_amount")#float(pe_e.total_amount)-float(pe_e.allocated_amount)
	elif payment_entry == "No":
		out_s+=frappe.db.get_value("Sales Invoice",{"name":bill_no},"outstanding_amount")

	return out_s
