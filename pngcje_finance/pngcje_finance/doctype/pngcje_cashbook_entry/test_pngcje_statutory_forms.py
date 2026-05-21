import frappe
from frappe.tests.utils import FrappeTestCase

class TestPNGCJEStatutoryForms(FrappeTestCase):
	def setUp(self):
		# Create dependencies
		if not frappe.db.exists("Supplier", "Air Niugini"):
			frappe.get_doc({"doctype": "Supplier", "supplier_name": "Air Niugini"}).insert()

		vote_code = frappe.db.get_value("Account", {"account_name": "Travel - Airfare (1118-121)"})
		cost_center = frappe.db.get_value("Cost Center", {"cost_center_name": "PNGCJE"})

		# Ensure we have a sample record
		if not frappe.db.exists("PNGCJE Cashbook Entry", "TEST-FORM-001"):
			doc = frappe.get_doc({
				"doctype": "PNGCJE Cashbook Entry",
				"name": "TEST-FORM-001",
				"naming_series": "PNGCJE-CASH-.2026.-.####",
				"date": "2026-05-21",
				"payee": "Air Niugini",
				"particulars": "Travel to Lae for workshop",
				"vote_activity_code": vote_code,
				"program_officer": frappe.db.get_value("Employee", {"employee_number": "PO-001"}),
				"target_audience": "JO-P",
				"cost_center": cost_center,
				"amount": 500
			})
			doc.flags.ignore_mandatory = True
			doc.insert()
			self.sample_doc = doc
		else:
			self.sample_doc = frappe.get_doc("PNGCJE Cashbook Entry", "TEST-FORM-001")

	def test_ff3_format_content(self):
		"""
		Check that the FF3 Print Format document has the correct HTML defined.
		"""
		pf = frappe.get_doc("Print Format", "PNGCJE FF3 - Requisition for Expenditure")
		self.assertIn("REQUISITION FOR EXPENDITURE (FF3)", pf.html)
		self.assertIn("{{ doc.payee }}", pf.html)

	def test_ff4_format_content(self):
		"""
		Check that the FF4 Print Format document has the correct HTML defined.
		"""
		pf = frappe.get_doc("Print Format", "PNGCJE FF4 - General Expenses")
		self.assertIn("GENERAL EXPENSES (FF4)", pf.html)
		self.assertIn("{{ doc.payee }}", pf.html)

	def test_rendering_manually(self):
		"""
		Manually render the Jinja to ensure it works.
		"""
		pf = frappe.get_doc("Print Format", "PNGCJE FF3 - Requisition for Expenditure")
		rendered = frappe.render_template(pf.html, {"doc": self.sample_doc})
		self.assertIn("REQUISITION FOR EXPENDITURE (FF3)", rendered)
		self.assertIn("Air Niugini", rendered)
