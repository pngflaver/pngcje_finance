import frappe

def create_workflow():
	# 1. Create Roles
	roles = [
		"PNGCJE Requisitioning Officer",
		"Financial Delegate",
		"Section 32 Officer",
		"Certifying Officer",
		"Payment Authorizer"
	]
	for role in roles:
		if not frappe.db.exists("Role", role):
			frappe.get_doc({"doctype": "Role", "role_name": role}).insert()
	
	# 2. Create Workflow States
	states = [
		"Draft",
		"Pending Funds Check",
		"Pending Sec 32 Approval",
		"Approved (Committed)",
		"Pending Claim Certification",
		"Ready for Payment"
	]
	for state in states:
		if not frappe.db.exists("Workflow State", state):
			frappe.get_doc({"doctype": "Workflow State", "workflow_state_name": state, "style": "Primary"}).insert()

	# 3. Create Workflow Actions
	actions = [
		"Submit for Funds Check",
		"Certify Funds",
		"Approve Expenditure",
		"Submit for Certification",
		"Certify Claim"
	]
	for action in actions:
		if not frappe.db.exists("Workflow Action Master", action):
			frappe.get_doc({"doctype": "Workflow Action Master", "workflow_action_name": action}).insert()

	# 4. Create Workflow
	workflow_name = "PNGCJE Cashbook Approval"
	if frappe.db.exists("Workflow", workflow_name):
		frappe.delete_doc("Workflow", workflow_name)
	
	workflow = frappe.get_doc({
		"doctype": "Workflow",
		"workflow_name": workflow_name,
		"document_type": "PNGCJE Cashbook Entry",
		"workflow_state_field": "workflow_state",
		"is_active": 1,
		"override_status": 1,
		"states": [
			{"state": "Draft", "doc_status": 0, "allow_edit": "PNGCJE Requisitioning Officer"},
			{"state": "Pending Funds Check", "doc_status": 0, "allow_edit": "Financial Delegate"},
			{"state": "Pending Sec 32 Approval", "doc_status": 0, "allow_edit": "Section 32 Officer"},
			# Once submitted, we allow the next officers in line to "edit" (which in Frappe submitted mode means "see buttons")
			{"state": "Approved (Committed)", "doc_status": 1, "allow_edit": "Certifying Officer"},
			{"state": "Pending Claim Certification", "doc_status": 1, "allow_edit": "Certifying Officer"},
			{"state": "Ready for Payment", "doc_status": 1, "allow_edit": "Payment Authorizer"}
		],
		"transitions": [
			{
				"state": "Draft",
				"action": "Submit for Funds Check",
				"next_state": "Pending Funds Check",
				"allowed": "PNGCJE Requisitioning Officer"
			},
			{
				"state": "Pending Funds Check",
				"action": "Certify Funds",
				"next_state": "Pending Sec 32 Approval",
				"allowed": "Financial Delegate"
			},
			{
				"state": "Pending Sec 32 Approval",
				"action": "Approve Expenditure",
				"next_state": "Approved (Committed)",
				"allowed": "Section 32 Officer"
			},
			{
				"state": "Approved (Committed)",
				"action": "Certify Claim",
				"next_state": "Ready for Payment",
				"allowed": "Certifying Officer"
			}
		]
	})
	workflow.insert()
	
	# 5. CRITICAL: Grant 'Submit' permission to Certifying Officer 
	# In Frappe, to move a Submitted doc to another state, the user needs 'Submit' permission on the DocType
	if not frappe.db.exists("Custom DocPerm", {"parent": "PNGCJE Cashbook Entry", "role": "Certifying Officer", "submit": 1}):
		frappe.db.sql("""update `tabCustom DocPerm` set submit=1, cancel=1 
			where parent='PNGCJE Cashbook Entry' and role in ('Certifying Officer', 'Payment Authorizer')""")

	frappe.db.commit()
	print(f"Workflow '{workflow_name}' updated successfully.")

if __name__ == "__main__":
	create_workflow()
