import frappe
from frappe import _
from frappe.model.document import Document

class PNGCJEProgramOfficerAllocation(Document):
	def validate(self):
		self.validate_total_allocation()

	def validate_total_allocation(self):
		total_monthly = sum(float(d.allocation_amount) for d in self.monthly_allocations)
		if total_monthly != float(self.annual_allocation):
			frappe.throw(_("Sum of monthly allocations ({0}) must equal annual allocation ({1})")
				.format(total_monthly, self.annual_allocation))
