# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import ValidationError

class StockChangeProductQty(models.TransientModel):
    _inherit = 'stock.change.product.qty'

    def change_product_qty(self):
        res = super(StockChangeProductQty, self).change_product_qty()
        if not self.env.user.has_group("ibos_update_qty_disable.group_onhand_qty_user"):
            raise ValidationError(
                _("You don't have access rights for update on hand quantity!"))
        return res



class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    def action_apply_all(self):
        res = super(StockQuant, self).action_apply_all()
        if not self.env.user.has_group("ibos_update_qty_disable.group_onhand_qty_user"):
            raise ValidationError(
                _("You don't have access rights for update on hand quantity! Please discard this operation"))
        return res
    
    def action_apply_inventory(self):
        if not self.env.user.has_group("ibos_update_qty_disable.group_onhand_qty_user"):
            raise ValidationError(
                _("You don't have access rights for update on hand quantity! Please discard this operation"))
        res = super(StockQuant, self).action_apply_inventory()
        return res

class StockInventoryAdjustmentName(models.TransientModel):
    _inherit = 'stock.inventory.adjustment.name'
    
    def action_apply(self):
        if not self.env.user.has_group("ibos_update_qty_disable.group_onhand_qty_user"):
            raise ValidationError(
                _("You don't have access rights for update on hand quantity! Please discard this operation"))
        res = super(StockInventoryAdjustmentName, self).action_apply()
        return res
