import frappe

def create_workflow():
	# 1. Create Roles
	roles = [
		"PNGCJE Requisitioning Officer",
		"Financial Delegate",
		"Section 32 Officer",
		"Examiner Officer",
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
		"Pending Payment Authorization",
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
		"Examine Claim",
		"Certify Claim",
		"Authorize Payment"
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
			{"state": "Approved (Committed)", "doc_status": 1, "allow_edit": "Examiner Officer"},
			{"state": "Pending Claim Certification", "doc_status": 1, "allow_edit": "Certifying Officer"},
			{"state": "Pending Payment Authorization", "doc_status": 1, "allow_edit": "Payment Authorizer"},
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
				"action": "Examine Claim",
				"next_state": "Pending Claim Certification",
				"allowed": "Examiner Officer"
			},
			{
				"state": "Pending Claim Certification",
				"action": "Certify Claim",
				"next_state": "Pending Payment Authorization",
				"allowed": "Certifying Officer"
			},
			{
				"state": "Pending Payment Authorization",
				"action": "Authorize Payment",
				"next_state": "Ready for Payment",
				"allowed": "Payment Authorizer"
			}
		]
	})
	workflow.insert()
	
	# 5. CRITICAL: Grant 'Submit' and 'Cancel' permissions to roles that act on submitted documents
	roles_to_permit = ["Section 32 Officer", "Examiner Officer", "Certifying Officer", "Payment Authorizer"]
	for role in roles_to_permit:
		if not frappe.db.exists("Custom DocPerm", {"parent": "PNGCJE Cashbook Entry", "role": role}):
			frappe.get_doc({
				"doctype": "Custom DocPerm",
				"parent": "PNGCJE Cashbook Entry",
				"parenttype": "DocType",
				"parentfield": "permissions",
				"role": role,
				"read": 1,
				"write": 1,
				"submit": 1,
				"cancel": 1,
				"print": 1,
				"email": 1,
				"permlevel": 0
			}).insert(ignore_permissions=True)
		else:
			frappe.db.sql("""
				UPDATE `tabCustom DocPerm` 
				SET submit=1, cancel=1, `write`=1 
				WHERE parent='PNGCJE Cashbook Entry' AND role=%s
			""", (role,))

	frappe.db.commit()
	print(f"Workflow '{workflow_name}' updated successfully.")

if __name__ == "__main__":
	create_workflow()

