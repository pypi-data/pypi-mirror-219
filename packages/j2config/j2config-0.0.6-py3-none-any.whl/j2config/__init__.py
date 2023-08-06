"""Package which helps simplifying text output generation from template. 
"""

__doc__ = '''Package which helps simplifying text output generation from template.'''


from .j2 import PrepareConfig
from .read_conditions import get_variables, get_conditions
from .data_collect import ABSRegion


__all__ = [
	'PrepareConfig',
	'get_conditions', 'get_variables',
	'ABSRegion'
	
]

__version__ = '0.0.6'