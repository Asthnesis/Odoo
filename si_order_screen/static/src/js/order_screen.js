/** @odoo-module */
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";

export class OrderScreen extends ReceiptScreen {
    static template = "pos_restaurant.OrderScreen";
    static components = { OrderReceipt, OrderScreenReceipt: 'OrderScreenReceipt' };

    constructor() {
        super(...arguments);
        patch(Order.prototype, {
            export_for_printing() {
                const lines = [...this.orderlines];
                const groupedObjects = lines.reduce((acc, line) => {
                    const { product } = line;
                    if (product.pos_categ_ids && product.pos_categ_ids.length > 0) {
                        const categoryId = product.pos_categ_ids[0];
                        const categoryName = this.pos.db.category_by_id[categoryId].name;
                        if (!acc[categoryName]) {
                            acc[categoryName] = { category_name: categoryName, lines: [] };
                        }
                        acc[categoryName].lines.push(line);
                    }
                    return acc;
                }, {});
                const result = Object.values(groupedObjects);
                const orderlines = super.export_for_printing();
                return {
                    ...orderlines,
                    orderlines: result,
                };
            },
        });
    }

    confirm() {
        if (!this.env.isMobile) {
            this.props.resolve({ confirmed: true, payload: null });
            this.pos.closeTempScreen();
        }
    }

    async printReceipt() {
        await super.printReceipt();
        this.currentOrder._printed = false;
    }

    get isBill() {
        return true;
    }
}

registry.category("pos_screens").add("OrderScreen", OrderScreen);
