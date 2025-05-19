# Empty file to make directory a Python package
from app import db
from .user import User
from .trip import Trip

__all__ = ['User', 'Trip']