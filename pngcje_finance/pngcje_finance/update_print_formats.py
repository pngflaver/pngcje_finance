import frappe

def update_print_formats():
	# CSS styling for forms (shared / included in both)
	style = """
	<style>
		@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&display=swap');
		
		.statutory-form {
			font-family: 'Outfit', 'Inter', sans-serif;
			color: #1a1a1a;
			line-height: 1.4;
			font-size: 11px;
			padding: 10px;
			box-sizing: border-box;
			width: 100%;
		}
		
		.header-container {
			text-align: center;
			margin-bottom: 12px;
			position: relative;
			border-bottom: 2px solid;
			padding-bottom: 6px;
		}
		.header-left {
			position: absolute;
			left: 0;
			top: 0;
			font-weight: 700;
			font-size: 12px;
		}
		.header-right {
			position: absolute;
			right: 0;
			top: 0;
			font-weight: 700;
			font-size: 12px;
			text-align: right;
		}
		.header-title {
			font-weight: 700;
			font-size: 16px;
			margin: 0;
			letter-spacing: 1px;
		}
		.header-subtitle {
			font-size: 13px;
			font-weight: 500;
			margin: 4px 0 0 0;
			text-transform: uppercase;
		}

		.meta-info-table {
			width: 100%;
			margin-bottom: 10px;
			border-collapse: collapse;
		}
		.meta-info-table td {
			padding: 4px;
			vertical-align: top;
			border: 1px solid #ddd;
		}
		
		.particulars-table {
			width: 100%;
			border-collapse: collapse;
			margin-bottom: 12px;
		}
		.particulars-table th, .particulars-table td {
			border: 1px solid #000;
			padding: 5px;
			text-align: left;
			vertical-align: top;
		}
		.particulars-table th {
			background-color: #f5f5f5;
			font-weight: 700;
			text-transform: uppercase;
			font-size: 10px;
		}
		
		.flex-row {
			display: flex;
			justify-content: space-between;
			margin-top: 10px;
		}
		.flex-col-left {
			width: 56%;
		}
		.flex-col-right {
			width: 42%;
		}
		
		.section-box {
			border: 1px solid #000;
			padding: 6px;
			margin-bottom: 10px;
			background-color: #fff;
		}
		.section-title {
			font-weight: 700;
			text-transform: uppercase;
			border-bottom: 1px solid #000;
			padding-bottom: 3px;
			margin-bottom: 5px;
			font-size: 10px;
		}
		
		.sig-block {
			border: 1px dashed #999;
			padding: 6px;
			margin-top: 8px;
			font-size: 10.5px;
			background-color: #fafafa;
		}
		.sig-title {
			font-weight: 700;
			margin-bottom: 4px;
		}
		
		.coding-table {
			width: 100%;
			border-collapse: collapse;
			margin-top: 4px;
		}
		.coding-table th, .coding-table td {
			border: 1px solid #000;
			padding: 3px;
			text-align: center;
			font-size: 10px;
		}
		.coding-table th {
			font-weight: 700;
			background-color: #eaeaea;
		}
		
		.right-aligned {
			text-align: right !important;
		}
		
		.bold-text {
			font-weight: 700;
		}

		.statutory-note {
			font-size: 9px;
			line-height: 1.3;
			color: #333;
			margin-top: 5px;
			font-style: italic;
		}

		.paying-office-table {
			width: 100%;
			border-collapse: collapse;
			margin-top: 8px;
			border: 2px solid #000;
		}
		.paying-office-table td {
			border: 1px solid #000;
			padding: 6px;
			vertical-align: top;
		}

		/* Theme Colors */
		.theme-green {
			border: 3px solid #1b4d3e;
			background-color: #f7fbf9;
		}
		.theme-green .header-container {
			border-color: #1b4d3e;
			color: #1b4d3e;
		}
		
		.theme-yellow {
			border: 3px solid #b8860b;
			background-color: #fffff4;
		}
		.theme-yellow .header-container {
			border-color: #b8860b;
			color: #b8860b;
		}
		
		@media print {
			body {
				background-color: #fff !important;
			}
			.theme-green, .theme-yellow {
				background-color: #fff !important;
				border-color: #000 !important;
			}
			.theme-green .header-container, .theme-yellow .header-container {
				border-color: #000 !important;
				color: #000 !important;
			}
			.sig-block {
				background-color: #fff !important;
			}
			.coding-table th, .particulars-table th {
				background-color: #f0f0f0 !important;
				-webkit-print-color-adjust: exact;
				print-color-adjust: exact;
			}
			.no-print {
				display: none !important;
			}
		}
	</style>
	"""

	# Jinja setup namespace parsing for Division/Fund/Activity/Item
	# This logic cleans the selected account code (vote_activity_code) and splits it into ACT and ITEM.
	account_parsing_jinja = """
	{% set ns = namespace(act="", item="") %}
	{% if doc.vote_activity_code %}
		{% set clean_code = doc.vote_activity_code.replace("(", "").replace(")", "").replace("[", "").replace("]", "") %}
		{% for chunk in clean_code.split(" ") %}
			{% if "-" in chunk %}
				{% set parts = chunk.split("-") %}
				{% if parts[0].isdigit() %}
					{% set ns.act = parts[0] %}
				{% endif %}
				{% if parts|length > 1 and parts[1].isdigit() %}
					{% set ns.item = parts[1] %}
				{% endif %}
			{% endif %}
		{% endfor %}
	{% endif %}
	"""

	ff3_html = style + account_parsing_jinja + """
	<!-- REQUISITION FOR EXPENDITURE (FF3) -->
	<div class="statutory-form theme-green">
		<div class="header-container">
			<div class="header-left">Finance Form 3</div>
			<div class="header-right">
				Requisition No: <span class="bold-text">{{ doc.name }}</span><br>
				<span style="font-size:9px; font-weight:normal;">Revised 3/79</span>
			</div>
			<h1 class="header-title">PAPUA NEW GUINEA</h1>
			<div class="header-subtitle">Requisition for Authority / Expenditure</div>
		</div>

		<table class="meta-info-table">
			<tr>
				<td style="width: 50%;">
					<span class="bold-text">To:</span> Director Finance (Financial Delegate)
				</td>
				<td style="width: 50%;">
					<span class="bold-text">From:</span> Department of PNGCJE
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<span class="bold-text">Subject:</span> Subject to availability of funds, purchase of the undermentioned goods/services is approved for delivery.<br>
					<span class="bold-text">Reasons:</span> {{ doc.items[0].description if doc.items else 'Operational expenditures' }} (See attached copies)
				</td>
			</tr>
		</table>

		<table class="particulars-table">
			<thead>
				<tr>
					<th style="width: 25%;">Supplier Address</th>
					<th style="width: 45%;">Particulars</th>
					<th style="width: 10%; text-align: center;">Qty</th>
					<th style="width: 10%; text-align: right;">Rate</th>
					<th style="width: 10%; text-align: right;">Amount</th>
				</tr>
			</thead>
			<tbody>
				{% for item in doc.items %}
				<tr>
					<td>
						{% if loop.first %}
							<span class="bold-text">{{ doc.payee }}</span>
						{% endif %}
					</td>
					<td>{{ item.description }}</td>
					<td style="text-align: center;">{{ item.qty | int }}</td>
					<td style="text-align: right;">{{ item.get_formatted('unit_price') }}</td>
					<td style="text-align: right;">{{ item.get_formatted('amount') }}</td>
				</tr>
				{% endfor %}
			</tbody>
			<tfoot>
				<tr>
					<th colspan="4" style="text-align: right;">TOTAL:</th>
					<th style="text-align: right; font-weight: bold;">{{ doc.get_formatted('amount') }}</th>
				</tr>
			</tfoot>
		</table>

		<div class="flex-row">
			<!-- LEFT COLUMN: Accounts & Initial approvals -->
			<div class="flex-col-left">
				<div class="section-box">
					<div class="section-title">Account Coding Block</div>
					<table class="coding-table">
						<thead>
							<tr>
								<th>DIV</th>
								<th>FN</th>
								<th>ACT</th>
								<th>ITEM</th>
								<th style="text-align: right;">AMOUNT</th>
							</tr>
						</thead>
						<tbody>
							<tr>
								<td>223</td>
								<td>1704</td>
								<td>{{ ns.act or "1118" }}</td>
								<td>{{ ns.item or "121" }}</td>
								<td style="text-align: right; font-weight: bold;">{{ doc.get_formatted('amount') }}</td>
							</tr>
						</tbody>
					</table>
					
					<div style="margin-top: 6px; font-size: 10px;">
						Subsequent Financial Year Estimate: ____________________<br>
						Cash Fund Cert. No. of Financial Delegate: <span class="bold-text">223-1101</span>
					</div>
				</div>

				<div class="sig-block">
					<div class="sig-title">1. Authorized Requisition Officer</div>
					I certify that this requisition is made in accordance with approved activities.
					<br><br>
					Signature: _______________________________ Date: {{ doc.get_formatted('date') }}<br>
					Name: <span class="bold-text">{{ doc.program_officer or '' }}</span><br>
					Designation: Deputy Executive Director / Program Officer
				</div>

				<div class="sig-block">
					<div class="sig-title">3. Approval of Section 32 Officer</div>
					<span style="font-size: 9px;">(Required for all requisitions exceeding K500)</span>
					<br>
					Status: [ &nbsp; ] Approved &nbsp; &nbsp; [ &nbsp; ] Not Approved
					<br><br>
					Signature: _______________________________ Date: _____/_____/_____<br>
					Designation: Section 32 Officer &nbsp; &nbsp; Designated Limit: K _______________
				</div>
			</div>

			<!-- RIGHT COLUMN: Commitments & Financial Delegate -->
			<div class="flex-col-right">
				<div class="section-box">
					<div class="section-title">Commitment Details</div>
					<table class="coding-table">
						<thead>
							<tr>
								<th style="text-align: left;">Goods/Services</th>
								<th style="text-align: right;">Est Cost</th>
								<th>Com't No</th>
							</tr>
						</thead>
						<tbody>
							{% set is_travel = "travel" in (doc.vote_activity_code | lower) or "airfare" in (doc.vote_activity_code | lower) %}
							<tr>
								<td style="text-align: left;">Travel Fare</td>
								<td style="text-align: right;">{{ doc.get_formatted('amount') if is_travel else "K0.00" }}</td>
								<td></td>
							</tr>
							<tr>
								<td style="text-align: left;">Excess Baggage</td>
								<td style="text-align: right;">K0.00</td>
								<td></td>
							</tr>
							<tr>
								<td style="text-align: left;">Accommodation</td>
								<td style="text-align: right;">K0.00</td>
								<td></td>
							</tr>
							<tr>
								<td style="text-align: left;">Goods and Services</td>
								<td style="text-align: right;">{{ doc.get_formatted('amount') if not is_travel else "K0.00" }}</td>
								<td></td>
							</tr>
						</tbody>
					</table>
					
					<div class="statutory-note">
						Note 1: Travel and Accommodation: Approved itinerary required.<br>
						Note 2: Goods & Services: Written quotations required if cost exceeds K500.
					</div>
				</div>

				<div class="sig-block">
					<div class="sig-title">2. Funds Available</div>
					I certify that funds are available in the specified allocation.
					<br><br>
					Signature: _______________________________ Date: _____/_____/_____<br>
					Designation: Financial Delegate / Commitment Clerk
				</div>

				<div class="sig-block">
					<div class="sig-title">4. Funds Committed</div>
					Requisition has been entered in the commitment register.
					<br><br>
					Signature: _______________________________ Date: _____/_____/_____<br>
					Designation: Commitment Clerk
				</div>
			</div>
		</div>
	</div>
	"""

	# ----------------------------------------------------
	# FF4 Print Format Design (individual claim sheets)
	# ----------------------------------------------------
	ff4_html = style + account_parsing_jinja + """
	<!-- GENERAL EXPENSES (FF4) -->
	{% for item in doc.items %}
	<div class="statutory-form theme-yellow" style="{% if not loop.last %}page-break-after: always;{% endif %} margin-bottom: 25px;">
		<div class="header-container">
			<div class="header-left">Finance Form 4</div>
			<div class="header-right">
				Reference No: <span class="bold-text">{{ doc.name }}</span><br>
				<span style="font-size:9px; font-weight:normal;">Reg. 36</span>
			</div>
			<h1 class="header-title">PAPUA NEW GUINEA</h1>
			<div class="header-subtitle">General Expenses Claim Voucher</div>
		</div>

		<table class="meta-info-table">
			<tr>
				<td style="width: 70%;">
					<span class="bold-text">Dr. to (Payee/Claimant):</span> {{ doc.payee }}
				</td>
				<td style="width: 30%;">
					<span class="bold-text">Date of Claim:</span> {{ doc.get_formatted('date') }}
				</td>
			</tr>
		</table>

		<table class="particulars-table">
			<thead>
				<tr>
					<th style="width: 60%;">Particulars</th>
					<th style="width: 10%; text-align: center;">Quantity</th>
					<th style="width: 15%; text-align: right;">Unit Rate</th>
					<th style="width: 15%; text-align: right;">Amount</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>{{ item.description }}</td>
					<td style="text-align: center;">{{ item.qty | int }}</td>
					<td style="text-align: right;">{{ item.get_formatted('unit_price') }}</td>
					<td style="text-align: right; font-weight: bold;">{{ item.get_formatted('amount') }}</td>
				</tr>
			</tbody>
			<tfoot>
				<tr>
					<th colspan="3" style="text-align: right;">TOTAL:</th>
					<th style="text-align: right; font-weight: bold;">{{ item.get_formatted('amount') }}</th>
				</tr>
			</tfoot>
		</table>

		<div class="flex-row">
			<div style="width: 50%;">
				<div class="section-box">
					<div class="section-title">Account Coding Details</div>
					<div style="font-size:9.5px; margin-bottom:4px;">Commitment Number: ________________________</div>
					<table class="coding-table">
						<thead>
							<tr>
								<th>Div</th>
								<th>F</th>
								<th>Act</th>
								<th>Item</th>
								<th style="text-align: right;">Amount</th>
							</tr>
						</thead>
						<tbody>
							<tr>
								<td>223</td>
								<td>1704</td>
								<td>{{ ns.act or "1118" }}</td>
								<td>{{ ns.item or "128" }}</td>
								<td style="text-align: right; font-weight: bold;">{{ item.get_formatted('amount') }}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
			
			<div style="width: 46%; margin-top: 10px;">
				<div style="border: 1px solid #bbb; padding: 8px; background-color: #fff; font-size:10px;">
					<span class="bold-text">Claimant Certification:</span><br>
					I certify that the above claim is correct and represents expenses actually incurred on official duty.
					<br><br>
					Signature of Claimant: ________________________________<br>
					Name: <span class="bold-text">{{ doc.payee }}</span>
				</div>
			</div>
		</div>

		<div class="sig-block" style="margin-top: 6px;">
			C.F.C No. <span class="bold-text">223-1101</span> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
			<span class="bold-text">Certification of Accuracy:</span> I certify that this account is correct and properly cast.
			<br><br>
			Signature: _________________________________________ Designation: ________________________________________
		</div>

		<h4 style="margin: 10px 0 4px 0; text-transform: uppercase; font-size: 10px; font-weight: bold;">To Be Completed by Paying Office</h4>
		<table class="paying-office-table">
			<tr>
				<td style="width: 50%; font-size: 9.5px;">
					Date of Registration: _______________________<br>
					[ &nbsp; ] Not previously paid &nbsp; &nbsp; &nbsp; [ &nbsp; ] F.D.'s signature verified<br>
					Examined By: _____________________________<br><br>
					<span class="bold-text">Public Finance (C & A) Act Certificate:</span><br>
					I certify that this account is correct within the meaning of Section 12(b) of the Public Finance (C & A) Act.
					<br><br>
					Signature: ___________________________ (Certifying Officer) &nbsp; &nbsp; Date: _____/_____/_____
				</td>
				<td style="width: 50%; font-size: 9.5px; background-color: #fafafa;" class="no-print-bg">
					<div style="text-align: center; font-weight: bold; font-size: 10px; margin-bottom: 6px; border-bottom: 1px solid #000; padding-bottom: 2px;">
						FOR OFFICIAL USE ONLY
					</div>
					Registration No: ______________________ Consecutive No: ______________________
					<br><br>
					<span class="bold-text">Acquittance / Receipt:</span><br>
					Received this _____ day of _________________ 20___ the sum of:<br>
					<span class="bold-text">Kina:</span> __________________________________________________________________________<br>
					<span class="bold-text">Toea:</span> __________________________________________________________________________
					<br><br>
					Recipient Signature: ______________________ Witness: ______________________
				</td>
			</tr>
		</table>
	</div>
	{% endfor %}
	"""

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
			print(f"SUCCESS: Print Format '{f['name']}' updated in database.")
		else:
			# If the print format record doesn't exist, create it from scratch!
			doc = frappe.get_doc({
				'doctype': 'Print Format',
				'name': f['name'],
				'doc_type': 'PNGCJE Cashbook Entry',
				'format_type': 'Jinja',
				'html': f['html'],
				'custom_format': 1,
				'standard': 'No'
			})
			doc.insert()
			print(f"SUCCESS: Print Format '{f['name']}' created in database.")
	
	frappe.db.commit()

if __name__ == "__main__":
	update_print_formats()
