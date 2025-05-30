/** @odoo-module */
import { FormController } from 'web.FormController';
import { Dialog } from 'web.Dialog';
import { rpc } from 'web.rpc';
import { _t } from 'web.core';


    const SaleOrderFormController = FormController.include({
        _onButtonConfirm: async function (ev) {
            // Prevent the default confirm action
            ev.preventDefault();
            ev.stopPropagation();

            const record = this.model.get(this.handle);

            // Fetch the sale order data, including the order lines
            const orderId = record.data.id;
            const result = await rpc.query({
                model: 'sale.order',
                method: 'get_order_line_breakdown',
                args: [orderId],
            });

            // Format the order line breakdown
            let content = "<p>Order Breakdown:</p><ul>";
            result.lines.forEach(line => {
                content += `<li>${line.name}: ${line.amount.toFixed(2)}</li>`;
            });
            content += `</ul><p><strong>Total:</strong> ${result.total.toFixed(2)}</p>`;

            // Show the confirmation dialog
            const dialog = new Dialog(this, {
                title: _t("Confirm Sale Order"),
                size: 'medium',
                $content: $('<div>').html(content),
                buttons: [
                    {
                        text: _t("Cancel"),
                        classes: "btn-secondary",
                        close: true, // Close the dialog
                    },
                    {
                        text: _t("Confirm"),
                        classes: "btn-primary",
                        close: true, // Close the dialog
                        click: () => {
                            // Proceed with the confirmation
                            this._rpc({
                                model: 'sale.order',
                                method: 'action_confirm',
                                args: [[orderId]],
                            }).then(() => {
                                this.reload(); // Reload the form after confirmation
                            });
                        },
                    },
                ],
            });

            dialog.open();
        },
    });

    return SaleOrderFormController;
