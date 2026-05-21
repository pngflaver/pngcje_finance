import frappe
from frappe.tests.utils import FrappeTestCase

class TestPNGCJECashbookEntry(FrappeTestCase):
	def test_required_fields_exist(self):
		"""
		Test that all required fields for the PNGCJE Cashbook Entry exist in the schema.
		"""
		doc = frappe.new_doc("PNGCJE Cashbook Entry")
		required_fields = [
			"date",
			"payee",
			"particulars",
			"vote_activity_code",
			"program_officer",
			"target_audience",
			"cost_center",
			"amount"
		]
		
		for field in required_fields:
			self.assertTrue(hasattr(doc, field), f"Field '{field}' missing from PNGCJE Cashbook Entry")

	def test_mandatory_fields_validation(self):
		"""
		Test that mandatory fields are enforced at the database level/validation level.
		"""
		doc = frappe.new_doc("PNGCJE Cashbook Entry")
		# Missing all fields
		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_amount_positive(self):
		"""
		Test that the amount must be greater than zero.
		"""
		# This test will likely fail initially because we haven't implemented the logic yet
		doc = frappe.new_doc("PNGCJE Cashbook Entry")
		doc.date = frappe.utils.nowdate()
		doc.amount = -100
		# We expect a validation error for negative amounts
		self.assertRaises(frappe.ValidationError, doc.insert)
