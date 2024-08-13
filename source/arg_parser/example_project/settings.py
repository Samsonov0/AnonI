import os

from source.schemes.default import Headers

'''
This is an example of one of the ways to create app settings.
You can use any convenient way

(!) Recommend to use data structures for save application settings:
• Data classes
• Pydantic-config
• etc
'''

HEADERS = Headers()
CURRENT_DIRECTORY = os.getcwd()
