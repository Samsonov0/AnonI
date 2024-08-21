import os

from source.schemes.default import Headers


"""
Use this file to set project variables.

(!) The set variables can be used in SETTINGS (from source.settings import SETTINGS)
"""

HEADERS = Headers()
CURRENT_DIRECTORY = os.getcwd()
JWT_SECRET = "DEFAULT"
JWT_ALGORITHM = "HS256"
