# -*- coding: utf-8 -*-
"""
    funnel

    Sale Oppurtunity Funnel

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import ModelView, ModelSQL, fields


__all__ = ['Funnel', ]


class Funnel(ModelSQL, ModelView):
    'Sale opportunity funnel'
    __name__ = 'sale.opportunity.funnel'

    name = fields.Char('Name', required=True, select=True)
    sequence = fields.Integer('Sequence', required=True, select=True)

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
