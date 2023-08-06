"""Command line interface"""

from .cli import CommandLineInterface, ControlledProperty, ControlledEvent

from importlib_metadata import version

__author__ = "Olivier Vincent"
__version__ = version("clivo")
