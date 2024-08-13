import json
from typing import get_type_hints

from pydantic import Json
from pydantic_core import PydanticUndefined


async def fill_scheme(handler, body):
    scheme = get_type_hints(handler).get('scheme')

    try:
        scheme_fields = scheme.__fields__
    except AttributeError:
        raise AttributeError(
            'Handler "{handler}" have to include used scheme name via annotations types'.format(
                handler=handler.__name__
            )
        )

    data = {}
    for field_name, field_info in scheme_fields.items():
        body_data = body.get(field_name)
        if field_info.annotation is Json and body_data is not None and isinstance(body_data, (list, dict)):
            body_data = json.dumps(body_data)

        if field_info.is_required and body_data is None:
            default_value = field_info.default

            if default_value is PydanticUndefined:
                raise ValueError(
                    'Field "{field}" is required and expected {annotation}, but did not receive any data'.format(
                        field=field_name, annotation=field_info.annotation.__name__
                    )
                )
            data[field_name] = field_info.default
        else:
            data[field_name] = body_data

    return scheme(**data)
