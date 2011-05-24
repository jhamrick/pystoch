"""
pystoch.core
------------

"""

__all__ = ['erps', 'pystochobj', 'queries']

import erps
from erps import binomial, exponential, flip, gamma, gaussian, poisson, uniform, sample_integer, uniform_draw
__all__.extend(['binomial', 'exponential', 'flip', 'gamma', 'gaussian', 'poisson', 'uniform', 'sample_integer', 'uniform_draw'])

import pystochobj
from pystochobj import PyStochObj
__all__.extend(['PyStochObj'])

import queries
from queries import RejectionQuery, MetropolisHastings
__all__.extend(['RejectionQuery', 'MetropolisHastings'])
