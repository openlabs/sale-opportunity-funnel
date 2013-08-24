# -*- coding: utf-8 -*-
"""
    funnel

    Sale Oppurtunity Funnel

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval


__all__ = ['Funnel', 'FunnelStage', 'SaleOpportunity', ]
__metaclass__ = PoolMeta


class Funnel(ModelSQL, ModelView):
    'Sale opportunity funnel'
    __name__ = 'sale.opportunity.funnel'

    name = fields.Char('Name', required=True, select=True)
    sequence = fields.Integer('Sequence', required=True, select=True)
    stages = fields.One2Many(
        'sale.opportunity.funnel.stage', 'funnel', 'Stages'
    )

    @classmethod
    def __setup__(cls):
        super(Funnel, cls).__setup__()
        cls._sql_constraints += [
            ('check_name',
                'UNIQUE(name)',
                'Name of a funnel must be unique.')
        ]
        cls._order.insert(0, ('sequence', 'ASC'))

    @staticmethod
    def default_sequence():
        return 10


class FunnelStage(ModelSQL, ModelView):
    'Sale opportunity funnel stage'
    __name__ = 'sale.opportunity.funnel.stage'

    name = fields.Char('Name', required=True, select=True)
    sequence = fields.Integer('Sequence', required=True, select=True)
    funnel = fields.Many2One(
        'sale.opportunity.funnel', 'Funnel', required=True, select=True
    )

    @classmethod
    def __setup__(cls):
        super(FunnelStage, cls).__setup__()
        cls._sql_constraints += [
            (
                'check_name',
                'UNIQUE(name, funnel)',
                'Name of a stage must be uniue to a funnel.'
            ),
            (
                'check_sequence',
                'UNIQUE(sequence, funnel)',
                'Two stages cannot have the same sequence in a funnel'
            )
        ]
        cls._order.insert(0, ('sequence', 'ASC'))

    @staticmethod
    def default_sequence():
        """
        Default value of sequence
        """
        return 10


class SaleOpportunity:
    """
    Sale Opportunity
    """
    __name__ = 'sale.opportunity'

    funnel = fields.Many2One(
        'sale.opportunity.funnel', 'Funnel', required=True, select=True,
    )
    stage = fields.Many2One(
        'sale.opportunity.funnel.stage', 'Stage', required=True,
        on_change_with=['funnel'],
        domain=[('funnel', '=', Eval('funnel'))], depends=['funnel'],
        select=True,
    )

    def on_change_with_stage(self):
        if self.funnel and self.funnel.stages:
            return self.funnel.stages[0].id
