import frappe
from frappe import _
from frappe.model.document import Document

class PNGCJECashbookEntry(Document):
	def validate(self):
		self.validate_amount()

	def validate_amount(self):
		if not self.amount or self.amount <= 0:
			frappe.throw(_("Amount must be greater than zero."))
