import traceback
from functools import wraps
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


def login_required(view_func):
    """
    This decorator is used to check if the user is logged in.
    it anly works with class based views
    """

    @wraps(view_func)
    def _wrapped_view_func(_self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise APIException("You must be logged in to perform this action.")
        else:
            return view_func(_self, request, *args, **kwargs)

    return _wrapped_view_func


def dict_values_to_upper(data):
    """
    This function is used to convert the value of the dictionary to upper case
    """
    try:
        if isinstance(data, dict):
            return {k: v.upper() if isinstance(v, str) else v for k, v in data.items()}
        if isinstance(data, list):
            return [
                {k: v.upper() if isinstance(v, str) else v for k, v in item.items()}
                for item in data
            ]
        else:
            raise APIException(
                f"Invalid data type. Expected 'dict' or 'list[dict]' but got '{type(data)}'"
            )
    except Exception as e:
        raise APIException(f"{e}. Raised in 'dict_values_to_upper()' function") from e


def dict_key_to_lower(data):
    """
    This function is used to convert the key of the dictionary to lower case
    """
    try:
        if isinstance(data, dict):
            return {k.lower(): v for k, v in data.items()}
        if isinstance(data, list):
            return [{k.lower(): v for k, v in item.items()} for item in data]
        else:
            raise APIException(
                f"Invalid data type. Expected 'dict' or 'list[dict]' but got '{type(data)}'"
            )
    except Exception as e:
        raise APIException(f"{e}. Raised in 'dict_key_to_lower()' function") from e


def convert_to_sql(condition: list[dict]) -> str:
    """
    This function is used to convert the condition to SQL query
    """

    # function to format the string if the operator is 'LIKE', 'NOT LIKE', 'IN', 'NOT IN'
    def formatCondition(operator: str, condition: str) -> str:
        if operator in ("LIKE", "NOT LIKE"):
            return f"'%{condition}%'"
        if operator in ("IN", "NOT IN"):
            items = [f"'{item.strip()}'" for item in condition.split(",")]
            return f"({','.join(items)})"
        return f"'{condition}'"

    try:
        query = ""
        for item in condition:
            if (
                (item["condition"] == "" or item["condition"] is None)
                and item["operator"] != "IS NULL"
                and item["operator"] != "IS NOT NULL"
            ):
                continue
            if item["dataType"].upper() == "VARCHAR2":
                if isinstance(item["field"], str):
                    formatted_condition = formatCondition(
                        item["operator"], item["condition"]
                    )
                    query += f'UPPER({item["field"]}) {item["operator"]} {formatted_condition} AND '
                elif isinstance(item["field"], list):
                    arr = [
                        f'UPPER({field}) {item["operator"]} {formatCondition(item["operator"], item["condition"])}'
                        for field in item["field"]
                    ]
                    query += f'({" OR ".join(arr)}) AND '

            elif item["dataType"].upper() == "DATE":
                query += f"""
                    UPPER({item["field"]}) {item["operator"]} TO_DATE(\'{item["condition"]}\', \'DD/MM/YYYY\') AND
                """
            elif item["dataType"].upper() == "NUMBER":
                query += f'{item["field"]} {item["operator"]} {item["condition"]} AND '
            else:
                query += f'UPPER({item["field"]}) {item["operator"]} {item["condition"]} AND '
        return query + "1 = 1"
    except Exception as e:
        raise APIException(f"{e}. Raised in 'convert_to_sql()'") from e
