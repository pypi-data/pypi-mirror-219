import os


def env_get_str(key: str, def_value: str = None) -> str:
    """
    Return the string value defined for *key* in the current operating environment.

    :param key: The key the value is associated with.
    :param def_value: The default value to return, if the key has not been defined.
    :return: The int value associated with the key.
    """
    result: str
    try:
        result = os.environ[key]
    except (KeyError, TypeError):
        result = def_value

    return result


def env_get_bool(key: str, def_value: bool = None) -> bool:
    """
    Return the boolean value defined for *key* in the current operating environment.

    :param key: The key the value is associated with.
    :param def_value: The default value to return, if the key has not been defined.
    :return: The boolean value associated with the key.
    """
    result: bool
    try:
        result = bool(os.environ[key])
    except (KeyError, TypeError):
        result = def_value

    return result


def env_get_int(key: str, def_value: int = None) -> int:
    """
    Return the int value defined for *key* in the current operating environment.

    :param key: The key the value is associated with.
    :param def_value: The default value to return, if the key has not been defined.
    :return: The int value associated with the key.
    """
    result: int
    try:
        result = int(os.environ[key])
    except (KeyError, TypeError):
        result = def_value

    return result


def env_get_float(key: str, def_value: float = None) -> float:
    """
    Return the float value defined for *key* in the current operating environment.

    :param key: The key the value is associated with.
    :param def_value: The default value to return, if the key has not been defined.
    :return: The float value associated with the key.
    """
    result: float
    try:
        result = int(os.environ[key])
    except (KeyError, TypeError):
        result = def_value

    return result


APP_PREFIX = env_get_str("PYPOMES_APP_PREFIX", "PYPOMES")
