import json

from source.arg_parser.example_project.settings import HEADERS
from source.dependencies import RequestData, ResponseData
from source.routers import DefaultRouter
from source.schemes import DefaultScheme
from source.utils.status_code import HTTP_200_OK

"""
Use DefaultRouter to create default router for your handlers.
You can set:
• name – Router name
• description – Router description
• prefix – Router prefix

(!) In future versions we are planning to add OpenAPI generator for your routers,
and these information will be using there.
"""


hello_world_router = DefaultRouter(
    name="Use this router to say Hello World!",  # Edit this one to set router name
    description="Hello?",  # Edit this one to set router description
    prefix="/api",  # With prefix: "/api/some_page", and without prefix: "/some_page"
)


@hello_world_router.get("/hello_world/")  # Use router.get("path") to create GET handler
async def say_hello_world(request_data: RequestData) -> ResponseData:
    """
    Recommend to use types annotation for handlers arguments and return data.
    In some cases this is required condition to use handlers
    """

    data = json.dumps({"data": f"Hello World!"})

    response_scheme = DefaultScheme(  # Use DefaultScheme to return application response
        status=HTTP_200_OK, body=data, headers=HEADERS
    )

    response_data = ResponseData(scheme=response_scheme)

    return response_data  # Just return DefaultScheme instance to return your response


@hello_world_router.get(
    "/hello_world/{name}"
)  # Use {name} syntax to indicate expected data in url
async def say_hello_world_to_name(request_data: RequestData) -> ResponseData:
    """
    Always set request_data: RequestData in your arguments, even you don't need use it right now.
    It's need to get url data and other request data
    """
    name = request_data.path_parameters().get("name")

    data = json.dumps({"data": f"Hello World! And hello {name}"})

    response_scheme = DefaultScheme(  # Use DefaultScheme to return application response
        status=HTTP_200_OK, body=data, headers=HEADERS
    )

    response_data = ResponseData(scheme=response_scheme)

    return response_data
