frappe.ui.form.on("Purchase Receipt", {
	refresh(frm) {
		setup_ceo_submit_gate(frm);
	},

	before_submit(frm) {
		return handle_before_submit_comparison(frm);
	},
});

frappe.ui.form.on("Purchase Receipt Item", {
	qty(frm) {
		debounced_setup_ceo_submit_gate(frm);
	},
	rejected_qty(frm) {
		debounced_setup_ceo_submit_gate(frm);
	},
	received_qty(frm) {
		debounced_setup_ceo_submit_gate(frm);
	},
	rate(frm) {
		debounced_setup_ceo_submit_gate(frm);
	},
	purchase_order_item(frm) {
		debounced_setup_ceo_submit_gate(frm);
	},
	items_remove(frm) {
		debounced_setup_ceo_submit_gate(frm);
	},
});

function patch_toolbar_actions(frm) {
	if (frm._ceo_submit_gate_patched) {
		return;
	}

	frm._ceo_submit_gate_patched = true;
	const original_can_submit = frm.toolbar.can_submit.bind(frm.toolbar);
	const original_can_save = frm.toolbar.can_save.bind(frm.toolbar);

	frm.toolbar.can_submit = function () {
		// Hide Submit while check is running and when non-CEO is blocked
		if (frm._ceo_gate_loading || frm._ceo_submit_blocked) {
			return false;
		}
		return original_can_submit();
	};

	frm.toolbar.can_save = function () {
		if (frm._ceo_submit_blocked && !frm.is_dirty()) {
			return false;
		}
		return original_can_save();
	};
}

function get_ceo_headline(status) {
	const has_qty = status.qty_items && status.qty_items.length;
	const has_rate = status.rate_items && status.rate_items.length;

	if (has_qty && has_rate) {
		return __(
			"Quantity or Rate exceeds Purchase Order. Only a user with CEO role can submit this GRN."
		);
	}
	if (has_rate) {
		return __(
			"Rate exceeds Purchase Order. Only a user with CEO role can submit this GRN."
		);
	}
	return __(
		"Quantity exceeds Purchase Order. Only a user with CEO role can submit this GRN."
	);
}

function fmt(value, precision = 3) {
	return frappe.format(flt(value), { fieldtype: "Float", precision: precision });
}

function fmt_pct(value) {
	return `${fmt(value, 2)}%`;
}

function highlight(condition, value_html) {
	if (!condition) {
		return value_html;
	}
	return `<span style="color:#e24c4c;font-weight:600">${value_html}</span>`;
}

function build_comparison_html(rows) {
	if (!rows || !rows.length) {
		return `<p>${__("No differences found.")}</p>`;
	}

	const header = `
		<tr>
			<th>${__("Row")}</th>
			<th>${__("Item")}</th>
			<th>${__("PO")}</th>
			<th>${__("Change")}</th>
			<th>${__("PO Qty")}</th>
			<th>${__("GRN Qty")}</th>
			<th>${__("Qty Diff")}</th>
			<th>${__("PO Rate")}</th>
			<th>${__("GRN Rate")}</th>
			<th>${__("Rate Diff")}</th>
			<th>${__("Rate %")}</th>
			<th>${__("PO Amount")}</th>
			<th>${__("GRN Amount")}</th>
			<th>${__("Amount Diff")}</th>
		</tr>
	`;

	const body = rows
		.map((row) => {
			const item_code = frappe.utils.escape_html(row.item_code || "");
			const item_name = frappe.utils.escape_html(row.item_name || "");
			const item_label =
				item_name && item_name !== item_code
					? `${item_code}<br><span class="text-muted">${item_name}</span>`
					: item_code;

			return `
				<tr>
					<td>${frappe.utils.escape_html(String(row.idx || ""))}</td>
					<td>${item_label}</td>
					<td>${frappe.utils.escape_html(row.purchase_order || "")}</td>
					<td>${frappe.utils.escape_html(row.change_type || "")}</td>
					<td>${fmt(row.po_qty)}</td>
					<td>${highlight(row.qty_exceeded, fmt(row.grn_qty))}</td>
					<td>${highlight(row.qty_exceeded, fmt(row.qty_diff))}</td>
					<td>${fmt(row.po_rate)}</td>
					<td>${highlight(row.rate_exceeded, fmt(row.grn_rate))}</td>
					<td>${highlight(row.rate_exceeded, fmt(row.rate_diff))}</td>
					<td>${highlight(row.rate_exceeded, fmt_pct(row.rate_increase_pct))}</td>
					<td>${fmt(row.po_amount, 2)}</td>
					<td>${highlight(row.amount_diff > 0, fmt(row.grn_amount, 2))}</td>
					<td>${highlight(row.amount_diff > 0, fmt(row.amount_diff, 2))}</td>
				</tr>
			`;
		})
		.join("");

	return `
		<p>${__("The following item(s) exceed Purchase Order values:")}</p>
		<div class="table-responsive" style="max-height:360px;overflow:auto">
			<table class="table table-bordered table-sm" style="margin-bottom:0;min-width:980px">
				<thead>${header}</thead>
				<tbody>${body}</tbody>
			</table>
		</div>
	`;
}

function show_po_comparison_dialog({
	rows,
	title,
	primary_label,
	on_primary,
	on_cancel,
	can_confirm = false,
	message = "",
}) {
	const footer_note = can_confirm
		? `<p class="text-muted" style="margin-top:12px">${__(
				"Review the differences and confirm to submit."
		  )}</p>`
		: `<p class="text-muted" style="margin-top:12px">${__(
				"Please ask a user with CEO role to review and submit."
		  )}</p>`;

	const dialog = new frappe.ui.Dialog({
		title: title || __("PO vs GRN Comparison"),
		size: "extra-large",
		fields: [
			{
				fieldtype: "HTML",
				fieldname: "comparison_html",
				options: `${
					message
						? `<p><b>${frappe.utils.escape_html(message)}</b></p>`
						: ""
				}${build_comparison_html(rows)}${footer_note}`,
			},
		],
		primary_action_label: primary_label || __("Close"),
		primary_action() {
			dialog.hide();
			if (on_primary) {
				on_primary();
			}
		},
	});

	if (can_confirm) {
		dialog.set_secondary_action_label(__("Cancel"));
		dialog.set_secondary_action(() => {
			dialog.hide();
			if (on_cancel) {
				on_cancel();
			}
		});
	}

	dialog.show();
	return dialog;
}

async function fetch_submit_restriction(frm) {
	const { message } = await frappe.call({
		method: "planetto_dev.purchase_receipt.get_submit_restriction",
		args: { doc: frm.doc },
	});
	return message || {};
}

function clear_form_alerts(frm) {
	frm.dashboard.clear_headline();
}

function set_single_alert(frm, text, color) {
	clear_form_alerts(frm);
	if (text) {
		frm.dashboard.set_headline_alert(text, color);
	}
}

let _ceo_gate_timer = null;
function debounced_setup_ceo_submit_gate(frm) {
	if (_ceo_gate_timer) {
		clearTimeout(_ceo_gate_timer);
	}
	_ceo_gate_timer = setTimeout(() => setup_ceo_submit_gate(frm), 300);
}

async function setup_ceo_submit_gate(frm) {
	const run_id = (frm._ceo_gate_run_id || 0) + 1;
	frm._ceo_gate_run_id = run_id;

	patch_toolbar_actions(frm);
	frm.remove_custom_button(__("Compare with PO"));

	if (frm.doc.docstatus !== 0 || frm.doc.is_return) {
		frm._ceo_gate_loading = false;
		frm._ceo_submit_blocked = false;
		clear_form_alerts(frm);
		frm.toolbar.set_primary_action();
		return;
	}

	// Hide Submit while server check is in progress (prevents race)
	frm._ceo_gate_loading = true;
	frm.toolbar.set_primary_action();

	let status = {};
	try {
		status = await fetch_submit_restriction(frm);
	} catch (e) {
		frm._ceo_gate_loading = false;
		frm.toolbar.set_primary_action();
		throw e;
	}

	if (frm._ceo_gate_run_id !== run_id) {
		return;
	}

	frm._ceo_gate_loading = false;
	frm._po_comparison_rows = status.rows || [];
	frm._po_comparison_has_exceeded = !!status.has_exceeded;
	frm._ceo_submit_blocked = !!status.restricted;

	if (!status.has_exceeded) {
		clear_form_alerts(frm);
		frm.show_submit_message();
		frm.toolbar.set_primary_action();
		return;
	}

	frm.add_custom_button(__("Compare with PO"), () => {
		show_po_comparison_dialog({
			rows: status.rows,
			title: __("PO vs GRN Comparison"),
			primary_label: __("Close"),
			can_confirm: false,
			message: status.message,
		});
	});

	if (status.restricted) {
		// Non-CEO: no Submit, red alert, no blue submit banner
		set_single_alert(frm, get_ceo_headline(status), "red");
		frm.toolbar.set_primary_action();
		return;
	}

	// CEO / Administrator with exceed: Submit allowed after comparison confirm
	set_single_alert(
		frm,
		__(
			"Quantity/Rate exceeds PO. Click Submit to review comparison and confirm."
		),
		"orange"
	);
	frm.toolbar.set_primary_action();
}

async function handle_before_submit_comparison(frm) {
	const status = await fetch_submit_restriction(frm);

	if (!status.has_exceeded) {
		return;
	}

	// Server decides restriction by role — do not trust client role checks alone
	if (status.restricted) {
		frappe.throw({
			title: __("CEO Role Required"),
			message:
				status.message ||
				__(
					"Quantity or Rate is increased beyond Purchase Order. Only users with CEO role can submit this GRN."
				),
		});
	}

	return new Promise((resolve, reject) => {
		show_po_comparison_dialog({
			rows: status.rows,
			title: __("Confirm Submit — PO Comparison"),
			primary_label: __("Confirm Submit"),
			can_confirm: true,
			message: __(
				"Values exceed Purchase Order. Please review details and confirm to submit."
			),
			on_primary() {
				resolve();
			},
			on_cancel() {
				reject(__("Submit cancelled"));
			},
		});
	});
}
