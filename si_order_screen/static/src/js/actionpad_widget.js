/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";

/**
 * @props partner
 */

patch(ActionpadWidget.prototype, {

    async submitOrder() {
        if (!this.clicked) {
            this.clicked = true;
            try {
                await this.pos.sendOrderInPreparationUpdateLastChange(this.currentOrder);

                console.log("VOILA FROM THE CUSTOM!!")
                //  this.pos.showTempScreen("OrderScreen");
            } finally {
                this.clicked = false;
            }
        }
    },

});
