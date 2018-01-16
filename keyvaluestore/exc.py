import json

def create_exception_response(status_code, error_message):
    return {
        'statusCode': status_code,
        'body': json.dumps({'error_message': error_message})

    }

class HTTPError(Exception):

    def __init__(self, status_code=500, error_message="Internal Server Error"):
        self.status_code = status_code
        self.error_message = error_message

    def as_response(self):
        return create_exception_response(self.status_code, self.error_message)


class ValidationError(HTTPError):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        self.status_code = 422
        self.error_message = f"{field}: {message}"