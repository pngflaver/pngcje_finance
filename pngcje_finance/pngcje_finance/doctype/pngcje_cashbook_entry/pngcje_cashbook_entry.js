// PNGCJE Cashbook Entry Client-Side Script
frappe.ui.form.on('PNGCJE Cashbook Entry', {
	validate: function(frm) {
		// We can do a quick check here too if we want, but usually server-side is enough.
		// If the server throws an error, Frappe should catch it.
	},
	amount: function(frm) {
		if (frm.doc.amount > 1000) {
			frappe.msgprint({
				title: __('Budget Alert'),
				indicator: 'orange',
				message: __('Note: This amount exceeds the standard monthly allocation of 1,000 PGK for most officers. Please ensure you have sufficient budget before saving.')
			});
		}
	}
});
