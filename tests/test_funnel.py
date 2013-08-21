# -*- coding: utf-8 -*-
"""
    test_funnel

    Test Funnel

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import sys
import os
DIR = os.path.abspath(os.path.normpath(os.path.join(
    __file__,
    '..', '..', '..', '..', '..', 'trytond'))
)
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
    test_depends
from trytond.transaction import Transaction


class FunnelTestCase(unittest.TestCase):
    '''
    Test Sale Opportunity Funnel module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('sale_opportunity_funnel')
        self.funnel = POOL.get('sale.opportunity.funnel')
        self.stage = POOL.get('sale.opportunity.funnel.stage')

    def test0005views(self):
        '''
        Test views.
        '''
        test_view('sale_opportunity_funnel')

    def test0006depends(self):
        '''
        Test depends.
        '''
        test_depends()

    def test_0010_create_funnel(self):
        '''
        Create funnel.
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            funnel1 = self.funnel.create(
                {
                    'name': 'Funnel 1',
                }
            )
            self.assert_(funnel1.id)
            self.assertEqual(funnel1.sequence, 10)

    def test0020funnel_constraint(self):
        '''
        Test funnel unique name constraint.
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            self.funnel.create(
                {
                    'name': 'Funnel 1',
                }
            )
            self.assertRaises(
                Exception, self.funnel.create,
                {
                    'name': 'Funnel 1',
                }
            )

    def test_0030_create_funnel_stage(self):
        """
        Tests creation of funnel stage
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            funnel1 = self.funnel.create(
                {
                    'name': 'Funnel 1',
                }
            )
            stage1 = self.stage.create(
                {
                    'name': 'Stage 1',
                    'funnel': funnel1.id,
                }
            )
            self.assert_(stage1.id)
            self.assertEqual(stage1.sequence, 10)

    def test_0040funnel_stage_constraint(self):
        """
        Tests that funnel stage cannot be created with duplicate name
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            funnel1 = self.funnel.create(
                {
                    'name': 'Funnel 1',
                }
            )
            self.stage.create(
                {
                    'name': 'Stage 1',
                    'sequence': 10,
                    'funnel': funnel1.id,
                }
            )
            self.assertRaises(
                Exception, self.stage.create,
                {
                    'name': 'Stage 1',
                    'sequence': 11,
                    'funnel': funnel1.id,
                }
            )

    def test_0050funnel_stage_sequence_constraint(self):
        """
        Tests that two stages cannot have same sequence in a funnel
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            funnel1 = self.funnel.create(
                {
                    'name': 'Funnel 1',
                }
            )
            self.stage.create(
                {
                    'name': 'Stage 1',
                    'sequence': 10,
                    'funnel': funnel1.id,
                }
            )
            self.assertRaises(
                Exception, self.stage.create,
                {
                    'name': 'Stage 1',
                    'sequence': 10,
                    'funnel': funnel1.id,
                }
            )


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(FunnelTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
