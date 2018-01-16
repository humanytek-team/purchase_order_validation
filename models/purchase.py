# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


from openerp import fields, api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    product_qty_total = fields.Float(
        compute='_compute_qty',
        string='Total product quantity')

    @api.depends('order_line.product_qty')
    def _compute_qty(self):
        for order in self:
            qty_total = 0.0
            for line in order.order_line:
                qty_total += line.product_qty
            order.update({
                'product_qty_total': qty_total,
            })

    @api.multi
    def button_confirm(self):
        super(PurchaseOrder, self).button_confirm()

        for order in self:

            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'
                        and order.product_qty_total <
                        self.env.user.company_id.po_double_validation_product_qty)\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                if order.state != 'purchase':
                    order.button_approve()
            else:
                order.write({'state': 'to approve'})

        return {}
