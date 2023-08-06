# PyResponse

PyResponse is a Python package that provides utility functions to create success and error responses in various Python frameworks.

## Purpose

The purpose of PyResponse is to simplify the process of generating success and error responses in web applications. It provides two main functions, `create_success_response()` and `create_error_response()`, which can be used to generate standardized response structures.

## Installation

To install PyResponse, you can use pip:

```bash
pip install pyresponse

```

## Usage

PyResponse can be used with different web frameworks, including Django, FastAPI, and Flask. Here's how you can use PyResponse in each framework:

### # Example usage

status_code = HTTPStatus.OK # or status_code = 200

### Django

1. Install PyResponse using pip as shown in the installation section.
2. Import the necessary functions from PyResponse in your Django views or API handlers.
3. Use the `create_success_response()` and `create_error_response()` functions to generate the desired responses.

```python
from pyresponse.response import create_success_response, create_error_response

def my_view(request):
    # Process the request and generate the necessary data
    data = ...

    # Generate a success response
    response = create_success_response(data=data, message='Success', status_code=200)
    return response

def my_api_view(request):
    try:
        # Process the request and generate the necessary data
        data = ...

        # Generate a success response with a custom serializer
        serializer = MySerializer()
        response = create_success_response(data=data, message='Success', serializer=serializer, status_code=200)
        return response
    except Exception as e:
        # Generate an error response
        response = create_error_response(message=str(e), status_code=500)
        return response
```

## FastAPI

1. Install PyResponse using pip as shown in the installation section.
2. Import the necessary functions from PyResponse in your FastAPI routes.
3. Use the `create_success_response()` and `create_error_response()` functions to generate the desired responses.

```python
from fastapi import FastAPI
from pyresponse.response import create_success_response, create_error_response

app = FastAPI()

@app.get("/success")
def success():
    data = {'key': 'value'}
    message = 'Success message'
    status_code = 200

    response = create_success_response(data=data, message=message, status_code=status_code)
    return response

@app.get("/error")
def error():
    message = 'Error message'
    status_code = 400

    response = create_error_response(message=message, status_code=status_code)
    return response
```

## Flask

1. Install PyResponse.response using pip as shown in the installation section.
2. Import the necessary functions from PyResponse in your Flask routes.
3. Use the `create_success_response()` and `create_error_response()` functions to generate the desired responses.

```python
from flask import Flask, jsonify
from pyresponse import create_success_response, create_error_response

app = Flask(__name__)

@app.route("/success")
def success():
    data = {'key': 'value'}
    message = 'Success message'
    status_code = 200

    response = create_success_response(data=data, message=message, status_code=status_code)
    return jsonify(response)

@app.route("/error")
def error():
    message = 'Error message'
    status_code = 400

    response = create_error_response(message=message, status_code=status_code)
    return jsonify(response)
```

## Serializer Support

PyResponse supports different serializers like Pydantic and marshmallow. The `create_success_response()` and `create_error_response()` functions accept an additional `serializer` parameter, which allows users to pass their chosen serializer for serializing the response data.

If a serializer is provided, the response data is serialized using that serializer's `dict()` method. Otherwise, the response data is returned as is.

This modification enables users to use different serializers based on their requirements. They can pass their serializer instance to the response functions when needed.

Here are examples using Pydantic and marshmallow serializers:

### Pydantic

```python
from pydantic import BaseModel
from pyresponse import create_success_response

class MyModel(BaseModel):
    success: bool
    message: str
    data: dict

# Example usage
serializer = MyModel
response = create_success_response(data={'foo': 'bar'}, message='Success', serializer=serializer)
```

### Marshmallow

```python
from marshmallow import Schema, fields
from pyresponse import create_success_response

class MySchema(Schema):
success = fields.Boolean()
message = fields.String()
data = fields.Dict()

# Example usage

serializer = MySchema()
response = create_success_response(data={'foo': 'bar'}, message='Success', serializer=serializer)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
