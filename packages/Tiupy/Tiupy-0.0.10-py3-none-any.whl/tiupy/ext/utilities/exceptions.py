class BadRequestException(Exception):
    """
    API Code: 400 Bad Request
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class UnauthorizedException(Exception):
    """
    API Code: 401 Unauthorized
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class ForbiddenException(Exception):
    """
    API Code: 403 Forbidden
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class NotFoundException(Exception):
    """
    API Code: 404 Not Found
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class MethodNotAllowedException(Exception):
    """
    API Code: 405 Method Not Allowed
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)
        

class RequestTimeoutException(Exception):
    """
    API Code: 408 Request Timeout
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class ConflictException(Exception):
    """
    API Code: 409 Conflict
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class LengthRequiredException(Exception):
    """
    API Code: 411 Length Required
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class UnsupportedMediaTypeException(Exception):
    """
    API Code: 415 Unsupported Media Type
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class UnprocessableEntityException(Exception):
    """
    API Code: 422 Unprocessable Entity
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class InternalServerErrorException(Exception):
    """
    API Code: 500 Internal Server Error
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class ServiceUnavailableException(Exception):
    """
    API Code: 503 Service Unavailable
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class GatewayTimeoutException(Exception):
    """
    API Code: 504 Gateway Timeout
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


def CheckException(api_code):
    if api_code == 400:
        raise BadRequestException("Bad request.")
    elif api_code == 401:
        raise UnauthorizedException("Unauthorized access.")
    elif api_code == 403:
        raise ForbiddenException("Access is forbidden.")
    elif api_code == 404:
        raise NotFoundException("Requested resource not found.")
    elif api_code == 408:
        raise RequestTimeoutException("Request timeout.")
    elif api_code == 409:
        raise ConflictException("Conflict.")
    elif api_code == 411:
        raise LengthRequiredException("Length required.")
    elif api_code == 415:
        raise UnsupportedMediaTypeException("Unsupported media type.")
    elif api_code == 422:
        raise UnprocessableEntityException("Unprocessable entity.")
    elif api_code == 500:
        raise InternalServerErrorException("Internal server error.")
    elif api_code == 503:
        raise ServiceUnavailableException("Service is temporarily unavailable.")
    elif api_code == 504:
        raise GatewayTimeoutException("Gateway timeout.")
