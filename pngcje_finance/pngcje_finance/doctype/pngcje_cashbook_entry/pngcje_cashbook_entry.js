// PNGCJE Cashbook Entry Client-Side Script
console.log("PNGCJE Cashbook Entry Script Loaded");

frappe.ui.form.on('PNGCJE Cashbook Entry', {
	onload: function(frm) {
		console.log("Form Loaded");
	},
	setup: function(frm) {
		// Set query for accounts to only show expense accounts
		frm.set_query('vote_activity_code', function() {
			return {
				filters: {
					'root_type': 'Expense',
					'is_group': 0
				}
			};
		});
	},
	validate: function(frm) {
		console.log("Validating Form...");
		calculate_total(frm);
	}
});

frappe.ui.form.on('PNGCJE Cashbook Item', {
	qty: function(frm, cdt, cdn) {
		calculate_row_and_total(frm, cdt, cdn);
	},
	unit_price: function(frm, cdt, cdn) {
		calculate_row_and_total(frm, cdt, cdn);
	},
	items_remove: function(frm) {
		calculate_total(frm);
	}
});

var calculate_row_and_total = function(frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	row.amount = flt(row.qty) * flt(row.unit_price);
	frm.refresh_field('items');
	calculate_total(frm);
};

var calculate_total = function(frm) {
	var total = 0;
	(frm.doc.items || []).forEach(function(item) {
		total += flt(item.amount);
	});
	frm.set_value('amount', total);

	console.log("CURRENT TOTAL: " + total);

	if (total > 1000) {
		// UNMISTAKABLE ALERT
		alert("BUDGET WARNING: Total is " + total + " PGK. This exceeds the 1,000 PGK limit!");
		
		frappe.msgprint({
			title: __('Budget Warning'),
			indicator: 'orange',
			message: __('The total amount (<b>{0}</b>) exceeds the standard 1,000 PGK limit.')
				.format(format_currency(total, 'PGK'))
		});
	}
};
