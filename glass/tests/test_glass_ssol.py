from .test_glass_common import TestGlassCommon


class TestSubSaleOrderLine(TestGlassCommon):
    def test_compute_area(self):
        # create a SSOL
        ssol = self.env['sale.order.line.sub'].create({
            'edge_height': '0',
            'edge_width': '0',
            'description': '',
            'multiplier': 1,
            'quantity': 1,
            'total': 0,
            'height': 1000,
            'width': 1000,
            'type': 'glass',
        })
        # check initial are_total value
        ssol.compute_area()
        self.assertEqual(ssol.area_total, 0,
                         'Bad initial value for area total')
        # choose add a glass product
        ssol.glass_front_id = self.glass_product_id
        ssol.compute_area()
        self.assertEqual(ssol.area_total, 90,
                         'Wrong area_total computation')
