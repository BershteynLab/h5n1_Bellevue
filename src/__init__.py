"""
H5N1 Bellevue Project - Spatial Risk Mapping Module

This package provides tools for creating spatial risk maps for H5N1 outbreaks
at the zip code level, designed for use by Bellevue Hospital Critical Care Unit.
"""

from .risk_map import RiskMap, create_sample_data
from . import data_utils

__version__ = '0.1.0'
__all__ = ['RiskMap', 'create_sample_data', 'data_utils']


