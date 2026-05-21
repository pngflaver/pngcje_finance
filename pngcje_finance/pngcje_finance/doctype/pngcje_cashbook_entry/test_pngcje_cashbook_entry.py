import frappe
from frappe.tests.utils import FrappeTestCase

class TestPNGCJECashbookEntry(FrappeTestCase):
	def setUp(self):
		# Create Company
		if not frappe.db.exists("Company", "PNGCJE"):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": "PNGCJE",
				"default_currency": "PGK"
			}).insert()
		
		# Create Root Account if needed
		if not frappe.db.exists("Account", "Temporary Accounts - PNGCJE"):
			frappe.db.sql("""insert into `tabAccount` (name, account_name, account_type, root_type, report_type, company, is_group) 
				values ('Temporary Accounts - PNGCJE', 'Temporary Accounts', 'Expense Account', 'Expense', 'Profit and Loss', 'PNGCJE', 1)""")

		# Create dependencies
		if not frappe.db.exists("Supplier", "Test Supplier"):
			frappe.get_doc({"doctype": "Supplier", "supplier_name": "Test Supplier"}).insert()
		
		if not frappe.db.exists("Account", "Test Account - PNGCJE"):
			frappe.db.sql("""insert into `tabAccount` (name, account_name, account_type, root_type, report_type, company, is_group, parent_account) 
				values ('Test Account - PNGCJE', 'Test Account', 'Expense Account', 'Expense', 'Profit and Loss', 'PNGCJE', 0, 'Temporary Accounts - PNGCJE')""")

		if not frappe.db.exists("Cost Center", "Test Cost Center - PNGCJE"):
			frappe.db.sql("""insert into `tabCost Center` (name, cost_center_name, company, is_group) 
				values ('Test Cost Center - PNGCJE', 'Test Cost Center', 'PNGCJE', 0)""")

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
		doc = frappe.new_doc("PNGCJE Cashbook Entry")
		doc.date = frappe.utils.nowdate()
		doc.amount = -100
		# We expect a validation error for negative amounts
		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_funds_validation(self):
		"""
		Test that an entry cannot be saved if it exceeds the officer's allocation for the month.
		"""
		# Create Gender
		if not frappe.db.exists("Gender", "Female"):
			frappe.get_doc({"doctype": "Gender", "gender": "Female"}).insert()

		# Create a Program Officer (Employee)
		officer_id = frappe.db.get_value("Employee", {"employee_number": "PO-001"})
		if not officer_id:
			employee = frappe.get_doc({
				"doctype": "Employee",
				"employee_number": "PO-001",
				"first_name": "Test",
				"last_name": "Officer",
				"gender": "Female",
				"date_of_birth": "1990-01-01",
				"date_of_joining": "2020-01-01"
			}).insert()
			officer_id = employee.name
		
		# Create an Allocation for the officer
		fiscal_year = str(frappe.utils.nowdate()[:4])
		if not frappe.db.exists("Fiscal Year", fiscal_year):
			frappe.get_doc({
				"doctype": "Fiscal Year",
				"year": fiscal_year,
				"year_start_date": f"{fiscal_year}-01-01",
				"year_end_date": f"{fiscal_year}-12-31"
			}).insert()

		# Ensure clean state for allocation
		frappe.db.delete("PNGCJE Program Officer Allocation", {"program_officer": officer_id})

		allocation = frappe.get_doc({
			"doctype": "PNGCJE Program Officer Allocation",
			"program_officer": officer_id,
			"fiscal_year": fiscal_year,
			"annual_allocation": 500,
			"monthly_allocations": [
				{"month": "January", "allocation_amount": 500}
			]
		}).insert()

		# Try to create a Cashbook Entry that exceeds the monthly allocation
		doc = frappe.new_doc("PNGCJE Cashbook Entry")
		doc.date = f"{fiscal_year}-01-15"
		doc.program_officer = officer_id
		doc.amount = 600 # Exceeds 500
		doc.payee = "Test Supplier"
		doc.particulars = "Test"
		doc.vote_activity_code = "Test Account - PNGCJE"
		doc.target_audience = "JO-P"
		doc.cost_center = "Test Cost Center - PNGCJE"

		# This should fail validation
		self.assertRaises(frappe.ValidationError, doc.insert)
