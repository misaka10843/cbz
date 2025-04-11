from enum import Enum


def default_attr(value: any) -> any:
    """
    Provides a default value based on the expected type of an attribute.

    Args:
        value (any): Expected type or class of the attribute.

    Returns:
        any: Default value appropriate for the specified type or class.
            - For Enum types: Returns the 'UNKNOWN' member if available, otherwise the first member.
            - For int or float: Returns -1.
            - For bool: Returns False.
            - For str: Returns an empty string.
            - For other types: Invokes the callable (assuming it's a function or callable object).
    """
    if issubclass(value, Enum):
        keys = [i.name for i in list(value)]
        return value['UNKNOWN' if 'UNKNOWN' in keys else 'STORY']
    elif value in (int, float):
        return -1
    elif value == bool:
        return False
    elif value == str:
        return ''
    else:
        return value()


def verify_attr(expected_type: any, key: str, value: any) -> None:
    """
    Verifies if the provided value matches the expected type.

    Args:
        expected_type (any): Expected type of the attribute.
        key (str): Name of the attribute.
        value (any): Value to be verified against the expected type.

    Raises:
        TypeError: If the provided value does not match the expected type.
    """
    if not isinstance(value, expected_type):
        raise TypeError(f'Expected type {expected_type} for attribute "{key}", but got {type(value)}')


def repr_attr(value: any) -> any:
    """
    Provides a representation of the attribute's value.

    Args:
        value (any): Value of the attribute.

    Returns:
        any: Representation of the attribute's value.
            - For Enum types: Returns the value of the Enum.
            - For other types: Returns the value itself.
    """
    if isinstance(value, Enum):
        return value.value
    return value
