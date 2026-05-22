import frappe

def fix_print_permissions():
	roles = [
		'PNGCJE Requisitioning Officer',
		'Financial Delegate',
		'Section 32 Officer',
		'Examiner Officer',
		'Certifying Officer',
		'Payment Authorizer'
	]
	
	for role in roles:
		frappe.db.sql("""
			UPDATE `tabCustom DocPerm` 
			SET `print` = 1, `email` = 1 
			WHERE `parent` = 'PNGCJE Cashbook Entry' AND `role` = %s
		""", (role,))
	
	frappe.db.commit()
	print("SUCCESS: Print and Email permissions enabled for all workflow roles.")

if __name__ == "__main__":
	fix_print_permissions()
