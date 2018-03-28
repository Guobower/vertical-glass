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
        # check initial area_total value
        ssol.compute_area()
        self.assertEqual(ssol.area_total, 0,
                         'Bad initial value for area total')
        # choose add a glass product
        ssol.glass_front_id = self.glass_product_id
        ssol.compute_area()
        self.assertEqual(ssol.area_total, 90,
                         'Wrong area_total computation')

    def test_compute_perimeter(self):
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
        # check initial perimeter value, should be 0 sinze no edge selected
        ssol.compute_perimeter()
        self.assertEqual(ssol.perimeter, 0,
                         'Bad initial value for perimeter')
        # alter edges perimeter should now be 1+1=2m^2
        ssol.edge_height = '1'
        ssol.edge_width = '1'
        ssol.compute_perimeter()
        self.assertEqual(ssol.perimeter, 2,
                         'Bad value for perimeter')
        # alter edges perimeter should now be 1+1+1+1=4m^2
        ssol.edge_height = '2'
        ssol.edge_width = '2'
        ssol.compute_perimeter()
        self.assertEqual(ssol.perimeter, 4,
                         'Bad value for perimeter')






