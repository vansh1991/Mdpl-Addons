import frappe


def get_posting_date(self,method=None):
	if self.payment_entries:
		for entries in self.payment_entries:
			if entries.payment_document == "Payment Entry":
				frappe.db.set_value(entries.payment_document,entries.payment_entry,"posting_date",self.date)


@frappe.whitelist()
def update_serial_no(self,method=None):
	if self.items:
		for item in self.items:
			serial_no=frappe.db.get_value("Purchase Invoice Item",{"parent":self.purchase_invoice,"item_code":item.item_code},"serial_no")
			if serial_no:
				frappe.log_error("serial_no",serial_no)
				item.serial_no=serial_no
