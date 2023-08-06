# Standard library imports
from typing import Any, Callable, Dict, List, Type, Union
import inspect
import json

# Third-party module imports
from pydantic import create_model, ValidationError, BaseModel, Field
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
import starlette.datastructures


class SpecificationError(Exception):
    ...
    
    
status_to_message = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    304: "Not Modified",
    307: "Temporary Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}




def dict_to_model(data: Dict[str, Any], name: str="DynamicModel") -> BaseModel:
    """Generate a Pydantic model from a dictionary."""

    if data == ...:
        data = {}
    
    annotations = {}
    for key, value in data.items():
        if isinstance(value, dict):
            annotations[key] = (dict_to_model(value, key), ...)
        elif isinstance(value, list) and len(value) == 1 and isinstance(value[0], dict):
            annotations[key] = (List[dict_to_model(value[0], key)], ...)
        else:
            annotations[key] = (value, ...)

    return create_model(name, **annotations)



def validate_content_type(request: Request, content_type):
    req_content_type = request.headers.get('Content-Type')

    if not req_content_type or content_type not in req_content_type:
        raise HTTPException(400, f'Invalid `Content-Type` header. Must be `{content_type}`')

async def get_request_body_as_bytes(request: Request) -> bytes:
    return await request.body()

async def get_request_body_as_json(request: Request):
    validate_content_type(request, "application/json")
    try:
        return await request.json()
    except json.decoder.JSONDecodeError as exception:
        print(exception)
        raise HTTPException(422, "Request body is not a valid JSON.")
    
async def get_request_body_as_form(request: Request) -> list[tuple[str, Any]]:
    validate_content_type(request, "multipart/form-data")
    try:
        form_data = await request.form()
        return form_data.multi_items()
    except Exception as e:
        raise HTTPException(422, "Request body is not a valid form.")

class ResourcePath:
    def __init__(self, path: str):
        self.path = path

    def __truediv__(self, other):
        return ResourcePath(self.path + '/' + other)

class TypedAPI:
    def __init__(self):
        self.app = Starlette()
        self.routes = []

    def http(self, func: Callable[..., Any]) -> Callable[..., Any]:

        # EXTRACTING INFO FROM DEFINITION
        method_name = func.__name__.upper()
        assert method_name in ["GET", "POST", "HEAD", "DELETE", "PUT", "PATCH", "OPTIONS", "TRACE", "CONNECT"]
        signature = inspect.signature(func)
        params = signature.parameters


        # RESOURCE PATH VALIDATOR
        assert 'resource_path' in params
        resource_path = params['resource_path'].annotation
        assert isinstance(resource_path, ResourcePath)
        path = resource_path.path


        # HEADERS VALIDATOR
        assert "headers" in params
        headers_spec = params['headers'].annotation
        headers_model = dict_to_model(headers_spec, name="Headers")


        # CONSTRUCT BODY VALIDATORS
        if "body" not in params:
            raise SpecificationError("Endpoint spec must have a body parameter.")

        req_body_spec = params['body'].annotation

        if req_body_spec in [..., bytes]:
            get_request_body = get_request_body_as_bytes

        elif req_body_spec == dict:
            get_request_body = get_request_body_as_json

        elif isinstance(req_body_spec, dict):
            body_spec = dict_to_model(req_body_spec, name="BodySpec")
            async def get_request_body(request: Request) -> dict:
                req_body = await get_request_body_as_json(request)
                try:
                    body_spec(**req_body)
                    return req_body
                except ValidationError as exception:
                    raise HTTPException(422, str(exception.errors()))

        elif req_body_spec == list:
            get_request_body = get_request_body_as_form

        elif isinstance(req_body_spec, list):
            field_dict = {name: (type_, ...) for name, type_ in req_body_spec}
            body_spec = create_model('BodySpec', **field_dict)
            async def get_request_body(request: Request) -> dict:
                req_body = await get_request_body_as_form(request)
                req_body_dict = {name: value for name, value in req_body}
                try:
                    body_spec(**req_body_dict)
                    return req_body
                except ValidationError as exception:
                    raise HTTPException(422, str(exception.errors()))
        else:
            raise NotImplementedError("Requested body spec is not implemented, nor is it a planned feature.")


        async def starlette_handler(request: Request):
            request_headers = dict(request.headers)
            
            try:
                request_headers_obj = headers_model(**request_headers)
            except ValidationError as exception:
                return JSONResponse(exception.errors())

            request_body = await get_request_body(request)
            status_code, response_headers, response_body = func(path, request_headers, request_body)
            
            if status_code == ...:
                status_code = 200

            if response_headers == ...:
                response_headers = None

            if response_body == ...:
                response_body = str(status_code) + " " + status_to_message[status_code]
                ResponseType = Response

            if isinstance(response_body, dict):
                ResponseType = JSONResponse

            response = ResponseType(response_body, status_code=status_code, headers=response_headers)
            return response

        route = Route(path, starlette_handler, methods=[method_name])
        self.routes.append(route)
        self.app.routes.append(route)
        return starlette_handler




if __name__ == "__main__":
    app = TypedAPI()
    v1 = ResourcePath("/api/v1")

    @app.http
    def get(
        resource_path: v1 / "a",
        headers: {
            'host': str
        },
        body: ...
    ):
        print("???", headers)
        return 200, ..., { "test": 123 }


    @app.http
    def post(
        resource_path: v1 / "a",
        headers: {
            'host': str
        },
        body: [
            ('test1', int),
            ('test2', str)
        ]
    ):
        print("???", headers)
        print("body??????", body)
        return 200, ..., { "test": 123 }


    
    
    import uvicorn
    uvicorn.run(app.app, host="0.0.0.0", port=8000)


    