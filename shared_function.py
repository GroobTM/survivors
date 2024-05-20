"""Shared Functions

This module containts functions shared across multiple modules moved to a 
separate file to prevent circular imports.
"""

__version__ = "0.1"
__author__ = "Reuben Wiles Maguire"

from numpy import hypot


def normalise(dx, dy):
    """Normalises a vector.
    
    Parameters
    ----------
    dx : float          - x component of vector
    dy : float          - y component of vector
    
    Return
    ------
    (float, float)      - normalised vector
    """

    hyp = hypot(dx, dy)
    if hyp != 0:
        return [dx, dy] / hyp
    else:
        return (0, 0)