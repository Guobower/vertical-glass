# -*- coding: utf-8 -*-
# (c) 2018 - AbAKUS IT SOLUTIONS

from openerp.exceptions import UserError, AccessError

from .test_glass_common import TestGlassCommon


class TestSaleOrder(TestGlassCommon):
    def test_sale_order(self):
        """
        Test the sale order flow
        """
        so = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'order_line': [(0, 0, {
                'name': p.name,
                'product_id': p.id,
                'product_uom_qty': 2,
                'product_uom': p.uom_id.id,
                'price_unit': p.list_price}) for p in self.products.values()],
            'pricelist_id': self.env.ref('product.list0').id,
        })
        self.assertEqual(so.amount_total, sum([0 * p.list_price for p in self.products.values()]),
                         'Sale: total amount is wrong')
        # so.order_line._compute_product_updatable()
        # self.assertTrue(so.order_line[0].product_updatable)
        # # send quotation
        # so.force_quotation_send()
        # self.assertTrue(so.state == 'sent', 'Sale: state after sending is wrong')
        # so.order_line._compute_product_updatable()
        # self.assertTrue(so.order_line[0].product_updatable)
        #
        # # confirm quotation
        # so.action_confirm()
        # self.assertTrue(so.state == 'sale')
        # self.assertTrue(so.invoice_status == 'to invoice')
        so.header_text = u"This is a text with company: %(company)s tag in it"
        self.assertEqual(so._get_header_text(),
                         ["<p>This is a text with company: YourCompany tag in it</p>"],
                         'Tag replacement failed')

