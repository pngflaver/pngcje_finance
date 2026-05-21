import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate

class PNGCJECashbookEntry(Document):
	def validate(self):
		self.validate_amount()
		self.validate_funds()

	def validate_amount(self):
		if not self.amount or self.amount <= 0:
			frappe.throw(_("Amount must be greater than zero."))

	def validate_funds(self):
		if not self.program_officer or not self.date:
			return

		# Get Month Name from Date
		posting_date = getdate(self.date)
		month_name = posting_date.strftime("%B")
		fiscal_year = str(posting_date.year)

		# Get Allocation
		allocation_name = frappe.db.get_value("PNGCJE Program Officer Allocation", {
			"program_officer": self.program_officer,
			"fiscal_year": fiscal_year
		})

		if not allocation_name:
			frappe.throw(_("No allocation found for Program Officer {0} in Fiscal Year {1}")
				.format(self.program_officer, fiscal_year))

		allocation_doc = frappe.get_doc("PNGCJE Program Officer Allocation", allocation_name)
		
		# Find monthly limit
		monthly_limit = 0
		for row in allocation_doc.monthly_allocations:
			if row.month == month_name:
				monthly_limit = float(row.allocation_amount)
				break
		
		if self.amount > monthly_limit:
			frappe.throw(_("Amount ({0}) exceeds the monthly allocation ({1}) for {2}")
				.format(self.amount, monthly_limit, month_name))
