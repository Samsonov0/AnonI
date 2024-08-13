from source.arg_parser.example_project.routers import hello_world_router, users_router
from source.app import Anoni

'''
Run this file to start web-app
'''

anoni = Anoni(
    app_name='Hello World!',  # Edit this parameter to edit the application name
    host='http://127.0.0.1',  # Edit this parameter to edit a host of the application
    port='8000',              # Edit this parameter to edit a port of the application
    log_level='info'          # Edit this parameter to edit a logging level of the application
)

anoni.register_router(hello_world_router)  # Use register_router method to register your handlers in router
anoni.register_router(users_router)        # Registration of "users" router

anoni.start_app()  # This is main row in this module. Use it to start your web-app
