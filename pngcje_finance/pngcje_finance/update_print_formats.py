import frappe

def update_print_formats():
	ff3_html = """<div style='padding: 20px; border: 2px solid green; background-color: #f0fff0;'>
    <div style='text-align: center;'>
        <h2>PNG Centre for Judicial Excellence</h2>
        <h3>REQUISITION FOR EXPENDITURE (FF3)</h3>
    </div>
    <hr>
    <table class='table table-bordered'>
        <tr><td><b>Payee:</b></td><td>{{ doc.payee }}</td></tr>
        <tr><td><b>Date:</b></td><td>{{ doc.get_formatted('date') }}</td></tr>
        <tr><td><b>Vote/Activity:</b></td><td>{{ doc.vote_activity_code }}</td></tr>
    </table>
    <h4>Itemized Particulars:</h4>
    <table class='table table-bordered'>
        <thead>
            <tr>
                <th>Description</th>
                <th class='text-right'>Qty</th>
                <th class='text-right'>Unit Price</th>
                <th class='text-right'>Total</th>
            </tr>
        </thead>
        <tbody>
            {% for item in doc.items %}
            <tr>
                <td>{{ item.description }}</td>
                <td class='text-right'>{{ item.qty }}</td>
                <td class='text-right'>{{ item.get_formatted('unit_price') }}</td>
                <td class='text-right'>{{ item.get_formatted('amount') }}</td>
            </tr>
            {% endfor %}
        </tbody>
        <tfoot>
            <tr>
                <th colspan='3' class='text-right'>Grand Total:</th>
                <th class='text-right'>{{ doc.get_formatted('amount') }}</th>
            </tr>
        </tfoot>
    </table>
    <br><br>
    <div class='row'>
        <div class='col-xs-4' style='border-top: 1px solid black;'>Requisitioning Officer</div>
        <div class='col-xs-4' style='border-top: 1px solid black;'>Financial Delegate</div>
        <div class='col-xs-4' style='border-top: 1px solid black;'>Section 32 Officer</div>
    </div>
</div>"""

	ff4_html = """<div style='padding: 20px; border: 2px solid #ffd700; background-color: #fffff0;'>
    <div style='text-align: center;'>
        <h2>PNG Centre for Judicial Excellence</h2>
        <h3>GENERAL EXPENSES (FF4)</h3>
    </div>
    <hr>
    <table class='table table-bordered'>
        <tr><td><b>Claimant:</b></td><td>{{ doc.payee }}</td></tr>
        <tr><td><b>Date:</b></td><td>{{ doc.get_formatted('date') }}</td></tr>
    </table>
    <h4>Claim Details:</h4>
    <table class='table table-bordered'>
        <thead>
            <tr>
                <th>Description</th>
                <th class='text-right'>Qty</th>
                <th class='text-right'>Total</th>
            </tr>
        </thead>
        <tbody>
            {% for item in doc.items %}
            <tr>
                <td>{{ item.description }}</td>
                <td class='text-right'>{{ item.qty }}</td>
                <td class='text-right'>{{ item.get_formatted('amount') }}</td>
            </tr>
            {% endfor %}
        </tbody>
        <tfoot>
            <tr>
                <th colspan='2' class='text-right'>Total Amount Due:</th>
                <th class='text-right'>{{ doc.get_formatted('amount') }}</th>
            </tr>
        </tfoot>
    </table>
    <br><br>
    <div class='row'>
        <div class='col-xs-4' style='border-top: 1px solid black;'>Claimant Signature</div>
        <div class='col-xs-4' style='border-top: 1px solid black;'>Certifying Officer</div>
        <div class='col-xs-4' style='border-top: 1px solid black;'>Authorized By</div>
    </div>
</div>"""

	formats = [
		{
			'name': 'PNGCJE FF3 - Requisition for Expenditure',
			'html': ff3_html
		},
		{
			'name': 'PNGCJE FF4 - General Expenses',
			'html': ff4_html
		}
	]

	for f in formats:
		if frappe.db.exists('Print Format', f['name']):
			doc = frappe.get_doc('Print Format', f['name'])
			doc.html = f['html']
			doc.save()
	
	frappe.db.commit()

if __name__ == "__main__":
	update_print_formats()
