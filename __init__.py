# -*- coding: utf-8 -*-
"""
    Initialize module

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from funnel import Funnel, FunnelStage, SaleOpportunity


def register():
    """
    Register models of a module.
    """
    Pool.register(
        Funnel,
        FunnelStage,
        SaleOpportunity,
        module='sale_opportunity_funnel', type_='model',
    )
