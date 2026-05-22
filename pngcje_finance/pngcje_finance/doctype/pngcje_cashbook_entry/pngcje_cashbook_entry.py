import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, fmt_money, flt

class PNGCJECashbookEntry(Document):
	def validate(self):
		self.calculate_total_amount()
		self.validate_amount()
		self.validate_funds()

	def calculate_total_amount(self):
		"""
		Calculates the total amount from the itemized list.
		"""
		total = 0
		for item in self.items:
			item.amount = flt(item.qty) * flt(item.unit_price)
			total += item.amount
		self.amount = total

	def validate_amount(self):
		if flt(self.amount) <= 0:
			frappe.throw(_("Total Amount must be greater than zero. Please add items with valid Price and Qty."))

	def validate_funds(self):
		# Auto-assign officer if missing and user is linked to one
		if not self.program_officer:
			employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user})
			if employee:
				self.program_officer = employee

		if not self.program_officer:
			frappe.throw(_("Please select a Program Officer to check budget availability."))

		if not self.date:
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
			frappe.throw(_("No budget allocation found for {0} in {1}. Save aborted.")
				.format(self.program_officer, fiscal_year))

		allocation_doc = frappe.get_doc("PNGCJE Program Officer Allocation", allocation_name)
		
		# Find monthly limit
		monthly_limit = 0
		for row in allocation_doc.monthly_allocations:
			if row.month == month_name:
				monthly_limit = flt(row.allocation_amount)
				break
		
		if flt(self.amount) > flt(monthly_limit):
			msg = _("<h3>Budget Limit Exceeded!</h3><hr>"
					"<b>Attempted Total:</b> {0}<br>"
					"<b>Monthly Limit ({1}):</b> {2}<br><br>"
					"Your transaction has been blocked. Please reduce the quantities or unit prices.") \
				.format(fmt_money(self.amount, "PGK"), month_name, fmt_money(monthly_limit, "PGK"))
			
			frappe.throw(msg=msg, title=_("Budget Enforcement"))
