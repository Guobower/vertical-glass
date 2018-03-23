# -*- coding: utf-8 -*-
# (c) 2018 - AbAKUS IT SOLUTIONS
from collections import OrderedDict
from openerp.tests import common


class TestGlassCommon(common.TransactionCase):

    def setUp(self):
        # make sur we run parent setUp
        super(TestGlassCommon, self).setUp()
        # chose users to run this test
        self.Users = self.env['res.users']

        #
        self.group_glass_manager_id = self.ref('base.group_sale_manager')
        self.group_glass_user_id = self.ref('base.group_sale_salesman')
        self.group_user_id = self.ref('base.group_user')

        # Will be used in various test cases of test_glass_flow
        self.demo_user_id = self.ref('base.user_demo')
        self.main_company_id = self.ref('base.main_company')
        self.main_partner_id = self.ref('base.main_partner')

        # Creating users and assigning group related to Glass Management/Sales/Regular employee
        self.res_users_glass_manager = self.Users.create({
            'company_id': self.main_company_id,
            'name': 'Glass Sales Manager',
            'login': 'glassm',
            'email': 'glassm@glasscompany.com',
            'groups_id': [(6, 0, [self.group_glass_manager_id])]
        })

        self.res_users_glass_officer = self.Users.create({
            'company_id': self.main_company_id,
            'name': 'Glass Sales Officer',
            'login': 'glasso',
            'email': 'glasso@glasscompany.com',
            'groups_id': [(6, 0, [self.group_glass_user_id])]
        })

        self.res_users_employee = self.Users.create({
            'company_id': self.main_company_id,
            'name': 'Glass Company Employee',
            'login': 'glasse',
            'email': 'glasse@glasscompany.com',
            'groups_id': [(6, 0, [self.group_user_id])]
        })

        # create quotation with different kinds of products (all possible combinations)
        self.products = OrderedDict([
            ('prod_order', self.env.ref('product.product_order_01')),
        ])

        self.partner = self.env.ref('base.res_partner_1')
