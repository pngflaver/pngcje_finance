// PNGCJE Cashbook Entry Client-Side Script
frappe.ui.form.on('PNGCJE Cashbook Entry', {
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
	refresh_field('items');
	calculate_total(frm);
};

var calculate_total = function(frm) {
	var total = 0;
	(frm.doc.items || []).forEach(function(item) {
		total += flt(item.amount);
	});
	frm.set_value('amount', total);

	if (total > 1000) {
		frappe.msgprint({
			title: __('Budget Alert'),
			indicator: 'orange',
			message: __('Note: This total (<b>{0}</b>) exceeds the standard monthly allocation of 1,000 PGK. Verification will happen on Save.')
				.format(format_currency(total, 'PGK'))
		});
	}
};
