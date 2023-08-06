from typing import Iterable
import base64


def jsonify_dict(source: dict):
    """
    Transforma os valores no dict *source* em valores que possam ser serializados em JSON, evitando *TypeError*:

    - *bytes* e *bytearray* são transformados em *str* formato *Base64*
    - *Iterable* é transformado em *list*
    - os outros tipos são mantidos
    HAZARD: dependendo do tipo de objeto contido em *source*, o resultado final poderá não ser serializável.

    :param source: o dict a ser tornado serializável
    """
    for key, value in source.items():
        if isinstance(value, dict):
            jsonify_dict(value)
        elif isinstance(value, bytes) or isinstance(value, bytearray):
            source[key] = base64.b64encode(value).decode()
        elif isinstance(value, Iterable) and not isinstance(value, str):
            source[key] = jsonify_iterable(value)


def jsonify_iterable(source: Iterable) -> list[any]:
    """
    Transforma os valores na lista *source* em valores que possam ser serializados em JSON, evitando *TypeError*:

    - *bytes* e *bytearray* são transformados em *str* formato *Base64*
    - *Iterable* é transformado em *list*
    - os outros tipos são mantidos
    HAZARD: dependendo do tipo de objeto contido em *source*, o resultado final poderá não ser serializável.

    :param source: a lista a ser tornada serializável
    """
    result: list[any] = []
    for value in source:
        if isinstance(value, dict):
            jsonify_dict(value)
            result.append(value)
        elif isinstance(value, bytes) or isinstance(value, bytearray):
            result.append(base64.b64encode(value).decode())
        elif isinstance(value, Iterable) and not isinstance(value, str):
            result.append(jsonify_iterable(value))
        else:
            result.append(value)

    return result
