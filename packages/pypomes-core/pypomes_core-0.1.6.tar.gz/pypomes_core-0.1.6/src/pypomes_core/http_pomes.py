
from typing import Final
import logging
import requests
import sys

from .exception_pomes import exc_format

# https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status

MIMETYPE_BINARY: Final[str] = "application/octet-stream"
MIMETYPE_CSS: Final[str] = "text/css"
MIMETYPE_CSV: Final[str] = "text/csv"
MIMETYPE_HTML: Final[str] = "text/html"
MIMETYPE_JAVASCRIPT: Final[str] = "text/javascript"
MIMETYPE_JSON: Final[str] = "application/json"
MIMETYPE_MULTIPART: Final[str] = "multipart/form-data"
MIMETYPE_PDF: Final[str] = "application/pdf"
MIMETYPE_PKCS7: Final[str] = "application/pkcs7-signature"
MIMETYPE_SOAP: Final[str] = "application/soap+xml"
MIMETYPE_TEXT: Final[str] = "text/plain"
MIMETYPE_URLENCODED: Final[str] = "application/x-www-form-urlencoded"
MIMETYPE_XML: Final[str] = "application/xml"
MIMETYPE_ZIP: Final[str] = "application/zip"


# TODO (add description)
__HTTP_STATUS: Final[dict] = {
  200: {
    "name": "OK",
    "description": ""
  },
  201: {
    "name": "CREATED",
    "description": ""
  },
  202: {
    "name": "ACCEPTED",
    "description": ""
  },
  203: {
    "name": "NON AUTHORITATIVE INFORMATION",
    "description": ""
  },
  204: {
    "name": "NO CONTENT",
    "description": ""
  },
  205: {
    "name": "RESET CONTENT",
    "description": ""
  },
  206: {
    "name": "PARTIAL CONTENT",
    "description": ""
  },
  300: {
    "name": "MULTIPLE CHOICE",
    "description": ""
  },
  301: {
    "name": "MOVED PERMANENTLY",
    "description": ""
  },
  302: {
    "name": "FOUND",
    "description": ""
  },
  303: {
    "name": "SEE OTHER",
    "description": ""
  },
  304: {
    "name": "NOT MODIFIED",
    "description": ""
  },
  305: {
    "name": "USE PROXY",
    "description": ""
  },
  307: {
    "name": "TEMPORARY REDIRECT",
    "description": ""
  },
  308: {
    "name": "PERMANENT REDIRECT",
    "description": ""
  },
  400: {
    "name": "BAD REQUEST",
    "description": ""
  },
  401: {
    "name": "UNAUTHORIZED",
    "description": ""
  },
  403: {
    "name": "FORBIDDEN",
    "description": ""
  },
  404: {
    "name": "NOT FOUND",
    "description": ""
  },
  405: {
    "name": "METHOD NOT ALLOWED",
    "description": ""
  },
  406: {
    "name": "NOT ACCEPTABLE",
    "description": ""
  },
  407: {
    "name": "AUTHENTICATION REQUIRED",
    "description": ""
  },
  408: {
    "name": "",
    "description": ""
  },
  409: {
    "name": "REQUEST TIMEOUT",
    "description": ""
  },
  410: {
    "name": "GONE",
    "description": ""
  },
  411: {
    "name": "LENGTH REQUIRED",
    "description": ""
  },
  412: {
    "name": "",
    "description": ""
  },
  413: {
    "name": "PAYLOAD TOO LARGE",
    "description": ""
  },
  414: {
    "name": "URI TOO LONG",
    "description": ""
  },
  500: {
    "name": "INTERNAL SERVER ERROR",
    "description": ""
  },
  501: {
    "name": "NOT IMPLEMENTED",
    "description": ""
  },
  502: {
    "name": "",
    "description": ""
  },
  503: {
    "name": "BAD GATEWAY",
    "description": ""
  },
  504: {
    "name": "GATEWAY TIMEOPUT",
    "description": ""
  },
  505: {
    "name": "",
    "description": ""
  },
  506: {
    "name": "VARIANT ALSO NEGOTIATES",
    "description": ""
  },
  507: {
    "name": "INSUFFICIENT STORAGE",
    "description": ""
  },
  508: {
    "name": "LOOP DETECTED",
    "description": ""
  },
  510: {
    "name": "NOT EXTENDED",
    "description": ""
  },
  511: {
    "name": "NETWORK AUTHENTICATION REQUIRED",
    "description": ""
  }
}


def http_status_name(status_code: int) -> str:

    item: dict = __HTTP_STATUS.get(status_code, {"name": "Unknown status code"})
    result = f"HTTP status code {status_code}: {item.get('name')}"
                                                             
    return result


def http_status_description(status_code: int) -> str:

    item: dict = __HTTP_STATUS.get(status_code, {"description": "Unknown status code"})
    result = f"HTTP status code {status_code}: {item.get('description')}"

    return result


def http_json_from_get(errors: list[str], url: str, headers: dict = None,
                       req_params: dict = None, logger: logging.Logger = None) -> dict:

    if logger is not None:
        logger.info(f"Invoking GET: '{url}'")

    # initialize return variable
    result: dict | None = None

    try:
        response: requests.Response = requests.get(url=url,
                                                   headers=headers,
                                                   params=req_params)
        if logger is not None:
            logger.info(f"Invoked '{url}', status: '{http_status_name(response.status_code)}'")
        result = response.json()
    except Exception as e:
        msg: str = f"Error invoking '{url}': '{exc_format(e, sys.exc_info())}'"
        if logger is not None:
            logger.info(msg)
        errors.append(msg)

    return result


def http_json_from_post(errors: list[str], url: str, headers: dict = None, req_params: dict = None,
                        req_data: dict = None, req_json: dict = None, logger: logging.Logger = None) -> dict:

    if logger is not None:
        logger.info(f"Invoking POST: '{url}'")

    # initialize return variable
    result: dict | None = None

    try:
        response: requests.Response = requests.post(url=url,
                                                    headers=headers,
                                                    data=req_data,
                                                    json=req_json,
                                                    params=req_params)
        if logger is not None:
            logger.info(f"Invoked '{url}', status: '{http_status_name(response.status_code)}'")
        result = response.json()
    except Exception as e:
        msg: str = f"Error invoking '{url}': '{exc_format(e, sys.exc_info())}'"
        if logger is not None:
            logger.info(msg)
        errors.append(msg)

    return result
