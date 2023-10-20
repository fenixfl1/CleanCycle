import traceback
from rest_framework.response import Response
from rest_framework.exceptions import APIException


def get_traceback():
    print(f"traceback: {traceback.format_exc()}")
    return traceback.format_exc()


def excep(func):
    """
    This decorator is used to catch the exception print the traceback and raise the exception
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exc_info = traceback.format_exc()
            get_traceback()
            raise APIException(
                f"{str(e)}. Raised in {func.__name__}. {exc_info}"
            ) from e

    return wrapper


def viewException(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIException as e:
            get_traceback()
            return Response({"error": str(e)}, status=e.status_code or 400)

    return wrapper
