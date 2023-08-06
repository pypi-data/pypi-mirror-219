"""
This Python module contains the custom exceptions.
"""


__all__ = ["ModelNotExistError"]
__version__ = ['1.0.0']
__author__ = ['Yuen Shing Yan Hindy']


class ModelNotExistError(Exception):
    """A custom exception or error that indicate a .tm model is not yet
    defined"""
