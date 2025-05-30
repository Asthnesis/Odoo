/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

// Create widget "smartButtonWidget", #Task:1394, #Jatin.
export class smartButtonWidget extends Component {
    setup() {
        this.actionService = useService("action");
        this.rpc = useService("rpc");
    }

    onClick() {
        var self = this;
        var method = "";
        self.rpc('/web/dataset/call_kw', {model: 'sale.order.line',
                    method: self.props.name == "product_sale_id_reference" ? "show_product_sale_lines" : "show_product_purchase_lines",
                    args: [0, this.props.value],
                    kwargs: {},
                }).then(function(action) {
                    self.actionService.doAction(action);
                });
    }
}
smartButtonWidget.template = "setu_product_price_history.buttonWidget";

smartButtonWidget.components = {
    smartButtonWidget,
    supportedTypes: ["integer"],
};

registry.category("fields").add("smartButtonWidget", smartButtonWidget);
