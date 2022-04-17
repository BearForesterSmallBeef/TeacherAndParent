from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.http import HTTP_STATUS_CODES


def handle_error(_self, err):
    """It helps preventing writing unnecessary
    try/except block though out the application
    """
    # UnprocessableEntity suppress ValidationError so restoring
    if isinstance(getattr(err, "exc"), ValidationError):
        err = getattr(err, "exc")
        err.messages = err.messages["json"]
    print(err.with_traceback(err.__traceback__))
    # Handle HTTPExceptions
    if isinstance(err, HTTPException):
        error = {
            "error": {
                "status": err.code,
                'message': getattr(
                    err, 'description', HTTP_STATUS_CODES.get(err.code, '')
                ),
            }
        }
        return jsonify(error), err.code
    if isinstance(err, ValidationError):
        messages = [f"{k}: {'. '.join(v)}" for k, v in err.messages.items()]
        error = {
            "error": {
                "status": 422,
                'message': ";".join(messages),
            }
        }
        return jsonify(error), 422
    # If msg attribute is not set,
    # consider it as Python core exception and
    # hide sensitive error info from end user
    if not getattr(err, 'message', None):
        error = {
            "error": {
                "status": 500,
                'message': 'Server has encountered some error',
            }
        }
        return jsonify(error), 500
    # Handle application specific custom exceptions
    return jsonify(**err.kwargs), err.http_status_code


class EntityNotFound(NotFound):
    description = "Not found"
