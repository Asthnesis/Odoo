/** @odoo-module **/

import { Component } from '@web/core/component';

export class LockToggleBehavior extends Component {
    toggleLock(record) {
        record.is_locked = !record.is_locked;
    }
}