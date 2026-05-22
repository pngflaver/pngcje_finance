import frappe
from frappe.tests.utils import FrappeTestCase

# test_dependencies = ["Gender", "Employee"]

class TestPNGCJEStatutoryForms(FrappeTestCase):
	def setUp(self):
		# Create Company
		if not frappe.db.exists("Company", "PNGCJE"):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": "PNGCJE",
				"default_currency": "PGK"
			}).insert()

		# Create Cost Center if missing
		if not frappe.db.exists("Cost Center", "PNGCJE - PNGCJE"):
			frappe.db.sql("""insert into `tabCost Center` (name, cost_center_name, company, is_group) 
				values ('PNGCJE - PNGCJE', 'PNGCJE', 'PNGCJE', 0)""")

		# Create Gender Male & Female
		if not frappe.db.exists("Gender", "Female"):
			frappe.get_doc({"doctype": "Gender", "gender": "Female"}).insert()
		if not frappe.db.exists("Gender", "Male"):
			frappe.get_doc({"doctype": "Gender", "gender": "Male"}).insert()

		# Create Employee
		if not frappe.db.exists("Employee", "PO-001"):
			frappe.get_doc({
				"doctype": "Employee",
				"employee_number": "PO-001",
				"first_name": "John",
				"last_name": "Emma",
				"gender": "Female",
				"date_of_birth": "1990-01-01",
				"date_of_joining": "2020-01-01",
				"company": "PNGCJE"
			}).insert()

		# Create Root Account if needed
		if not frappe.db.exists("Account", "Temporary Accounts - PNGCJE"):
			frappe.db.sql("""insert into `tabAccount` (name, account_name, account_type, root_type, report_type, company, is_group) 
				values ('Temporary Accounts - PNGCJE', 'Temporary Accounts', 'Expense Account', 'Expense', 'Profit and Loss', 'PNGCJE', 1)""")

		# Create Account
		if not frappe.db.exists("Account", "Travel - Airfare (1118-121) - PNGCJE"):
			frappe.db.sql("""insert into `tabAccount` (name, account_name, account_type, root_type, report_type, company, is_group, parent_account) 
				values ('Travel - Airfare (1118-121) - PNGCJE', 'Travel - Airfare (1118-121)', 'Expense Account', 'Expense', 'Profit and Loss', 'PNGCJE', 0, 'Temporary Accounts - PNGCJE')""")

		# Create dependencies
		if not frappe.db.exists("Supplier", "Air Niugini"):
			frappe.get_doc({"doctype": "Supplier", "supplier_name": "Air Niugini"}).insert()

		# Create Fiscal Year
		fiscal_year = "2026"
		if not frappe.db.exists("Fiscal Year", fiscal_year):
			frappe.get_doc({
				"doctype": "Fiscal Year",
				"year": fiscal_year,
				"year_start_date": f"{fiscal_year}-01-01",
				"year_end_date": f"{fiscal_year}-12-31"
			}).insert()

		officer_id = frappe.db.get_value("Employee", {"employee_number": "PO-001"})

		# Create Allocation
		if officer_id and not frappe.db.exists("PNGCJE Program Officer Allocation", {"program_officer": officer_id, "fiscal_year": fiscal_year}):
			frappe.get_doc({
				"doctype": "PNGCJE Program Officer Allocation",
				"program_officer": officer_id,
				"fiscal_year": fiscal_year,
				"annual_allocation": 10000,
				"monthly_allocations": [
					{"month": "May", "allocation_amount": 10000}
				]
			}).insert()

		# Setup Print Formats
		from pngcje_finance.pngcje_finance.update_print_formats import update_print_formats
		update_print_formats()

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
				"vote_activity_code": vote_code,
				"program_officer": frappe.db.get_value("Employee", {"employee_number": "PO-001"}),
				"target_audience": "JO-P",
				"cost_center": cost_center,
				"items": [
					{
						"description": "Travel to Lae",
						"qty": 1,
						"unit_price": 500
					}
				]
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
		self.assertIn("{% for item in doc.items %}", pf.html)

	def test_ff4_format_content(self):
		"""
		Check that the FF4 Print Format document has the correct HTML defined.
		"""
		pf = frappe.get_doc("Print Format", "PNGCJE FF4 - General Expenses")
		self.assertIn("GENERAL EXPENSES (FF4)", pf.html)
		self.assertIn("{% for item in doc.items %}", pf.html)

	def test_rendering_manually(self):
		"""
		Manually render the Jinja to ensure it works.
		"""
		pf = frappe.get_doc("Print Format", "PNGCJE FF3 - Requisition for Expenditure")
		rendered = frappe.render_template(pf.html, {"doc": self.sample_doc})
		self.assertIn("REQUISITION FOR EXPENDITURE (FF3)", rendered)
		self.assertIn("Travel to Lae", rendered)
		self.assertIn("Air Niugini", rendered)

	def test_ff4_rendering_manually(self):
		"""
		Manually render the FF4 Jinja to ensure it works.
		"""
		pf = frappe.get_doc("Print Format", "PNGCJE FF4 - General Expenses")
		rendered = frappe.render_template(pf.html, {"doc": self.sample_doc})
		self.assertIn("GENERAL EXPENSES (FF4)", rendered)
		self.assertIn("Travel to Lae", rendered)
		self.assertIn("Air Niugini", rendered)

	def test_rendering_with_workflow_stamps(self):
		"""
		Create workflow comments and verify that the stamps are rendered in the HTML.
		"""
		# Clean comments for sample_doc
		frappe.db.delete("Comment", {"reference_doctype": "PNGCJE Cashbook Entry", "reference_name": self.sample_doc.name})

		# Create mock workflow comments
		comments = [
			{"content": "Pending Funds Check", "owner": "req_officer@example.com"},
			{"content": "Pending Sec 32 Approval", "owner": "fin_delegate@example.com"},
			{"content": "Approved (Committed)", "owner": "sec32_officer@example.com"},
			{"content": "Pending Claim Certification", "owner": "examiner_officer@example.com"},
			{"content": "Pending Payment Authorization", "owner": "cert_officer@example.com"},
			{"content": "Ready for Payment", "owner": "pay_authorizer@example.com"}
		]
		for comment in comments:
			frappe.get_doc({
				"doctype": "Comment",
				"comment_type": "Workflow",
				"reference_doctype": "PNGCJE Cashbook Entry",
				"reference_name": self.sample_doc.name,
				"content": comment["content"],
				"owner": comment["owner"]
			}).insert()

		# Render FF3 and assert stamps exist
		pf_ff3 = frappe.get_doc("Print Format", "PNGCJE FF3 - Requisition for Expenditure")
		rendered_ff3 = frappe.render_template(pf_ff3.html, {"doc": self.sample_doc})
		self.assertIn("DIGITALLY SIGNED / SUBMITTED", rendered_ff3)
		self.assertIn("FUNDS CERTIFIED", rendered_ff3)
		self.assertIn("SEC 32 APPROVED", rendered_ff3)
		self.assertIn("COMMITTED", rendered_ff3)

		# Render FF4 and assert stamps exist
		pf_ff4 = frappe.get_doc("Print Format", "PNGCJE FF4 - General Expenses")
		rendered_ff4 = frappe.render_template(pf_ff4.html, {"doc": self.sample_doc})
		self.assertIn("ACCURACY CERTIFIED", rendered_ff4)
		self.assertIn("EXAMINED", rendered_ff4)
		self.assertIn("SEC 12(b) CERTIFIED", rendered_ff4)
		self.assertIn("PAYMENT AUTHORIZED", rendered_ff4)
