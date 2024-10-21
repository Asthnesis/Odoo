odoo.define('si_pos_orderline.Orderline', function (require) {
    'use strict';

    const Orderline = require('point_of_sale.Orderline');
    const Registries = require('point_of_sale.Registries');
    const Order = require('point_of_sale.models').Order;

    const siOrderline = (Orderline) => class siOrderline extends Orderline {
        constructor(attr, options) {
            super(...arguments);
        }
    };

    const siOrder = (Order) => class siOrder extends Order {
        add_product(product, options) {
            super.add_product(...arguments);
            this._assignSequenceNumber();
        }

        remove_orderline(orderLine) {
            super.remove_orderline(...arguments);
            this._assignSequenceNumber(); 
        }

        _assignSequenceNumber() {
            const orderLines = this.get_orderlines();

            orderLines.forEach((line, index) => {
                line.custom_sequence_number = index + 1;
            });
        }
    };

    Registries.Component.extend(Orderline, siOrderline);
    Registries.Model.extend(Order, siOrder);

    return siOrderline;
});
