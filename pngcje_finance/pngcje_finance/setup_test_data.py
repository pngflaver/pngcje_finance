import frappe
from frappe.utils import nowdate

def setup_test_data():
	print("Starting Test Data Setup...")
	
	# 1. Company
	company_name = "PNGCJE"
	if not frappe.db.exists("Company", company_name):
		company = frappe.get_doc({
			"doctype": "Company",
			"company_name": company_name,
			"default_currency": "PGK"
		}).insert()
		print(f"Created Company: {company_name}")
	
	# 2. Fiscal Year
	fiscal_year = str(nowdate()[:4])
	if not frappe.db.exists("Fiscal Year", fiscal_year):
		frappe.get_doc({
			"doctype": "Fiscal Year",
			"year": fiscal_year,
			"year_start_date": f"{fiscal_year}-01-01",
			"year_end_date": f"{fiscal_year}-12-31"
		}).insert()
		print(f"Created Fiscal Year: {fiscal_year}")

	# 3. Supporting Records
	if not frappe.db.exists("Supplier", "Sample Supplier"):
		frappe.get_doc({"doctype": "Supplier", "supplier_name": "Sample Supplier"}).insert()
	
	# Handle Cost Center - PNGCJE
	if not frappe.db.exists("Cost Center", f"PNGCJE - {company_name}"):
		frappe.db.sql(f"""insert into `tabCost Center` (name, cost_center_name, company, is_group) 
			values ('PNGCJE - {company_name}', 'PNGCJE', '{company_name}', 0)""")

	# Handle Account
	if not frappe.db.exists("Account", f"Travel - 1118-121 - {company_name}"):
		frappe.db.sql(f"""insert into `tabAccount` (name, account_name, account_type, root_type, report_type, company, is_group) 
			values ('Travel - 1118-121 - {company_name}', 'Travel - 1118-121', 'Expense Account', 'Expense', 'Profit and Loss', '{company_name}', 0)""")

	# 4. Define Test Users and Roles
	test_users = [
		{
			"email": "req_officer@example.com",
			"first_name": "John",
			"last_name": "Emma",
			"role": "PNGCJE Requisitioning Officer",
			"emp_id": "PO-001"
		},
		{
			"email": "fin_delegate@example.com",
			"first_name": "Michael",
			"last_name": "Pits",
			"role": "Financial Delegate",
			"emp_id": "FD-001"
		},
		{
			"email": "sec32_officer@example.com",
			"first_name": "Secretary",
			"last_name": "NJSS",
			"role": "Section 32 Officer",
			"emp_id": "S32-001"
		},
		{
			"email": "cert_officer@example.com",
			"first_name": "Finance",
			"last_name": "Officer A",
			"role": "Certifying Officer",
			"emp_id": "CO-001"
		},
		{
			"email": "pay_authorizer@example.com",
			"first_name": "Finance",
			"last_name": "Director",
			"role": "Payment Authorizer",
			"emp_id": "PA-001"
		}
	]

	# Create Gender if missing
	if not frappe.db.exists("Gender", "Male"):
		frappe.get_doc({"doctype": "Gender", "gender": "Male"}).insert()

	for u in test_users:
		# Create User
		if not frappe.db.exists("User", u["email"]):
			user = frappe.get_doc({
				"doctype": "User",
				"email": u["email"],
				"first_name": u["first_name"],
				"last_name": u["last_name"],
				"new_password": "zMqumk7!Complex",
				"send_welcome_email": 0,
				"roles": [{"role": "Desk User"}]
			}).insert()
			print(f"Created User: {u['email']}")
		
		# Add specific role
		user = frappe.get_doc("User", u["email"])
		user.add_roles(u["role"])

		# Create Employee
		officer_id = frappe.db.get_value("Employee", {"employee_number": u["emp_id"]})
		if not officer_id:
			employee = frappe.get_doc({
				"doctype": "Employee",
				"employee_number": u["emp_id"],
				"first_name": u["first_name"],
				"last_name": u["last_name"],
				"gender": "Male",
				"company": company_name,
				"user_id": u["email"],
				"status": "Active",
				"date_of_joining": nowdate(),
				"date_of_birth": "1990-01-01"
			}).insert()
			print(f"Created Employee: {u['emp_id']}")
			officer_id = employee.name

	# 5. Create Allocation for John Emma (PO-001)
	officer_name = frappe.db.get_value("Employee", {"employee_number": "PO-001"})
	current_month = frappe.utils.getdate().strftime("%B")
	
	# Clean old allocation
	frappe.db.delete("PNGCJE Program Officer Allocation", {"program_officer": officer_name})
	
	frappe.get_doc({
		"doctype": "PNGCJE Program Officer Allocation",
		"program_officer": officer_name,
		"fiscal_year": fiscal_year,
		"annual_allocation": 1000,
		"monthly_allocations": [
			{"month": current_month, "allocation_amount": 1000}
		]
	}).insert()
	print(f"Created Allocation for John Emma for {current_month}: 1000 PGK")

	frappe.db.commit()
	print("Test Data Setup Complete.")

if __name__ == "__main__":
	setup_test_data()
