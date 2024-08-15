from source.arg_parser.example_project.schemes import UserModel
from source.arg_parser.example_project.settings import HEADERS
from source.dependencies import RequestData, ResponseData
from source.routers import DefaultRouter
from source.schemes import DefaultScheme
from source.utils.status_code import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

"""
Information specified in "hello_world.py " it will not be re-described.
Look for a description of previously unaffected functionality in this file.
"""

users_router = DefaultRouter(
    name="Use this router to operate users",
    description="Router for do some things with users",
    prefix="/api/users",
)

_temp_memory: dict[str: UserModel] = dict()


@users_router.get("")  # You can set empty path to connect handler to prefix path (base router path)
async def get_all_users(request_data: RequestData) -> ResponseData:
    response_scheme = DefaultScheme(  # Use DefaultScheme to set application response
        status=HTTP_200_OK, body=_temp_memory, headers=HEADERS
    )

    response_data = ResponseData(  # Use ResponseData to return response
        scheme=response_scheme
    )

    return response_data


@users_router.get("/{user_id}")
async def get_all_users(request_data: RequestData) -> ResponseData:
    user_id = request_data.path_parameters().get("user_id")

    user_data = _temp_memory.get(user_id)

    if user_data is not None:
        response_scheme = DefaultScheme(  # Use DefaultScheme to set application response
            status=HTTP_200_OK, body=user_data, headers=HEADERS
        )
    else:
        response_scheme = DefaultScheme(
            status=HTTP_400_BAD_REQUEST,
            headers=HEADERS,
            body={"message": "Data not found"},
        )

    response_data = ResponseData(
        scheme=response_scheme
    )

    return response_data


@users_router.post("")  # Use router.post("path") to create POST handler
async def add_new_user(scheme: UserModel, request_data: RequestData) -> ResponseData:
    """
    Use scheme: YourScheme (pydantic model) to set expected input data.
    For example UserModel:
    • id: int
    • name: str
    • age: int
    • data: Json
    """
    new_user_data = scheme.dict()

    _temp_memory[str(scheme.id)] = new_user_data

    response_scheme = DefaultScheme(status=HTTP_200_OK, headers=HEADERS, body=new_user_data)

    response_data = ResponseData(
        scheme=response_scheme
    )

    return response_data


@users_router.delete("{user_id}")  # Use router.delete("path") to create DELETE handler
async def delete_user(request_data: RequestData) -> ResponseData:
    user_id = request_data.path_parameters().get("user_id")

    if _temp_memory.get(user_id) is not None:
        _temp_memory.pop(user_id)

    response_scheme = DefaultScheme(
        status=HTTP_204_NO_CONTENT,
        headers=HEADERS,
    )

    response_data = ResponseData(
        scheme=response_scheme
    )

    return response_data


@users_router.put("{user_id}")  # Use router.put("path") to create PUT handler
async def edit_user(scheme: UserModel, request_data: RequestData):
    user_id = request_data.path_parameters().get("user_id")

    new_user_data = scheme.dict()

    if _temp_memory.get(user_id) is not None:
        _temp_memory[user_id] = new_user_data

    response_scheme = DefaultScheme(status=HTTP_200_OK, headers=HEADERS, body=new_user_data)

    response_data = ResponseData(
        scheme=response_scheme
    )

    return response_data
