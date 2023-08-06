import json
from datetime import date, datetime
from typing import Final
from .env_pomes import APP_PREFIX, env_get_str

VALIDATION_MSG_LANGUAGE: Final[str] = env_get_str(f"{APP_PREFIX}_VALIDATION_MSG_LANGUAGE", "pt")
VALIDATION_MSG_PREFIX: Final[str] = env_get_str(f"{APP_PREFIX}_VALIDATION_MSG_PREFIX", APP_PREFIX)


# valida o valor do atributo de acordo com lista e restrições de comprimento
def validate_value(value: str | int | float, min_val: int = None,
                   max_val: int = None, default: bool | list[any] = None) -> str:

    # inicializa variável de retorno
    result: str | None = None
    # 'value' pode ser None, e None pode estar em 'default'
    if isinstance(default, list):
        if value not in default:
            if value is None:
                result = __format_error(10)
            else:
                length: int = len(default)
                if length == 1:
                    result = __format_error(15, value, default[0])
                else:
                    # o último elemento da lista é None ?
                    if default[-1] is None:
                        # sim, omita-o da mensagem
                        length -= 1
                    result = __format_error(16, value, [default[:length]])
    elif value is None:
        if isinstance(default, bool) and default:
            result = __format_error(10)
    elif isinstance(value, str):
        length: int = len(value)
        if min_val is not None and max_val == min_val and length != min_val:
            result = __format_error(14, value, min_val)
        elif max_val is not None and max_val < length:
            result = __format_error(13, value, max_val)
        elif min_val is not None and length < min_val:
            result = __format_error(12, value, min_val)
    elif (min_val is not None and value < min_val) or \
         (max_val is not None and value > max_val):
        result = __format_error(17, value, [min_val, max_val])

    return result


# obtem e valida booleano - valor retornado pode ser None
def validate_bool(errors: list[str], scheme: dict, attr: str,
                  default: bool = None, mandatory: bool = False, parse_string: bool = False) -> bool:

    result: bool | None = None
    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        if parse_string:
            result = json.loads(scheme[suffix].lower())
        else:
            result = scheme[suffix]

        if not isinstance(result, bool):
            stat = __format_error(18, result, "bool")
    except (KeyError, TypeError):
        if default is not None:
            result = default
        elif mandatory:
            stat = __format_error(10)

    if stat is not None:
        errors.append(f"{stat} @{attr}")

    return result


# obtem e valida inteiro - valor retornado pode ser None
def validate_int(errors: list[str], scheme: dict, attr: str,
                 min_value: int = None, max_value: int = None,
                 default: bool | int | list[int] = None) -> int:

    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]

    # obtem e valida o valor
    result: int | None = scheme.get(suffix)
    if result is not None and \
       (not isinstance(result, int) or isinstance(result, bool)):
        stat = __format_error(18, result, "int")
    # bool é subtipo de int
    elif isinstance(default, int) and not isinstance(default, bool):
        if result is None:
            result = default
        else:
            stat = validate_value(result, min_value, max_value)
    else:
        stat = validate_value(result, min_value, max_value, default)

    if stat is not None:
        errors.append(f"{stat} @{attr}")

    return result


# obtem e valida decimal - valor retornado pode ser None
def validate_float(errors: list[str], scheme: dict, attr: str,
                   min_value: float = None, max_value: float = None,
                   default: bool | float | list[float | int] = None) -> float:

    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]

    # obtem e valida o valor
    result: float | None = scheme.get(suffix)
    if result is not None and not isinstance(result, int) and not isinstance(result, float):
        stat = __format_error(18, result, "float")
    else:
        # bool é subtipo de int
        if isinstance(result, int) and not isinstance(result, bool):
            result = float(result)
        if isinstance(default, float):
            if result is None:
                result = default
            else:
                stat = validate_value(result, min_value, max_value)
        else:
            stat = validate_value(result, min_value, max_value, default)

    if stat is not None:
        errors.append(f"{stat} @{attr}")

    return result


# obtem e valida string - valor retornado pode ser None
def validate_str(errors: list[str], scheme: dict, attr: str,
                 min_length: int = None, max_length: int = None,
                 default: bool | str | list[str] = None) -> str:

    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]

    # obtem e valida o valor
    result: str = scheme.get(suffix)
    if result is not None and not isinstance(result, str):
        stat = __format_error(18, result, "str")
    elif isinstance(default, str):
        if result is None:
            result = default
        else:
            stat = validate_value(result, min_length, max_length)
    else:
        stat = validate_value(result, min_length, max_length, default)

    if stat is not None:
        errors.append(f"{stat} @{attr}")

    return result


# obtem e valida data - valor retornado pode ser None
def validate_date(errors: list[str], scheme: dict, attr: str,
                  default: bool | date = None, day_first: bool = True) -> date:

    # import needed module
    from .datetime_pomes import date_parse

    result: date | None = None
    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        date_str: str = scheme[suffix]
        result = date_parse(date_str, dayfirst=day_first)
        if result is None:
            stat = __format_error(11, date_str)
        elif result > datetime.now().date():
            stat = __format_error(19, date_str)
    except KeyError:
        if isinstance(default, bool) and default:
            stat = __format_error(10)
        elif isinstance(default, date):
            result = default

    if stat is not None:
        errors.append(f"{stat} @{attr}")

    return result


# obtem e valida data - valor retornado pode ser None
def validate_datetime(errors: list[str], scheme: dict, attr: str,
                      default: bool | datetime = None, day_first: bool = True) -> datetime:

    # import needed module
    from .datetime_pomes import datetime_parse

    result: datetime | None = None
    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        date_str: str = scheme[suffix]
        result = datetime_parse(date_str, dayfirst=day_first)
        if result is None:
            stat = __format_error(21, date_str)
        elif result > datetime.now():
            stat = __format_error(18, date_str)
    except KeyError:
        if isinstance(default, bool) and default:
            stat = __format_error(10)
        elif isinstance(default, datetime):
            result = default

    if stat is not None:
        errors.append(f"{stat} @{attr}")

    return result


# obtem e valida lista de inteiros - valor retornado pode ser None ou lista vazia
def validate_ints(errors: list[str], scheme: dict, attr: str,
                  min_size: int = None, max_size: int = None, mandatory: bool = False) -> list[int]:

    result: list[any] | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        values: list[any] = scheme[suffix]
        if isinstance(values, list):
            result = []
            if len(values) == 0:
                raise KeyError
            else:
                for inx, value in enumerate(values):
                    result.append(value)
                    if isinstance(value, int):
                        stat: str = validate_value(value, min_size, max_size)
                    else:
                        stat: str = __format_error(18, value, "int")
                    if stat is not None:
                        errors.append(f"{stat} @{attr}[{inx+1}]")
        else:
            errors.append(__format_error(18, result, "list", f"@{attr}"))
    except (KeyError, TypeError):
        if mandatory:
            errors.append(__format_error(10, f"@{attr}"))

    return result


# obtem e valida lista de strings - valor retornado pode ser None ou uma lista vazia
def validate_strs(errors: list[str], scheme: dict, attr: str,
                  min_size: int, max_size: int, mandatory: bool = False) -> list[str]:

    result: list[any] | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        values: list[any] = scheme[suffix]
        if isinstance(values, list):
            result = []
            if len(values) == 0:
                raise KeyError
            else:
                for inx, value in enumerate(values):
                    result.append(value)
                    if isinstance(value, str):
                        stat: str = validate_value(value, min_size, max_size)
                    else:
                        stat: str = __format_error(18, value, "str")
                    if stat is not None:
                        errors.append(f"{stat} @{attr}[{inx+1}]")
        else:
            errors.append(__format_error(18, result, "list", f"@{attr}"))
    except (KeyError, TypeError):
        if mandatory:
            errors.append(__format_error(11, f"@{attr}"))

    return result


def validate_format_error(error_id: int, err_msgs: dict, *args) -> str:

    # inicializa a variável de retorno
    result: str = VALIDATION_MSG_PREFIX + str(error_id) + ": " + err_msgs.get(error_id)

    if result is not None:
        # aplica os argumentos fornecidos
        for arg in args:
            if arg is None:
                result = result.replace(" {}", "", 1)
            elif isinstance(arg, str) and arg.startswith("@"):
                result += " " + arg
            elif isinstance(arg, str) and arg.find(" ") > 0:
                result = result.replace("{}", arg, 1)
            else:
                result = result.replace("{}", f"'{str(arg)}'", 1)

    return result


# formata itens na lista de erros: <codigo> <descricao> [@<atributo>]
def validate_format_errors(errors: list[str]) -> list[dict]:

    # import needed modulo
    from .str_pomes import str_find_whitespace

    # inicializa a variável de retorno
    result: list[dict] = []

    # extrai código, descrição e atributo do texto
    for error in errors:
        # localiza o último indicador do atributo
        pos = error.rfind("@")

        # existe whitespace no nome do atributo ?
        if pos > 0 and str_find_whitespace(error[pos:]) > 0:
            # sim, desconsidere-o
            pos = -1

        # o texto contem o atributo ?
        if pos == -1:
            # não
            out_error: dict = {}
            desc: str = error
        else:
            # sim
            term: str = "attribute" if VALIDATION_MSG_LANGUAGE == "en" else "atributo"
            out_error: dict = {term: error[pos + 1:]}
            desc = error[:pos - 1]

        # o texto contem o código ?
        if desc.startswith(VALIDATION_MSG_PREFIX):
            # sim
            term: str = "code" if VALIDATION_MSG_LANGUAGE == "en" else "codigo"
            out_error[term] = desc[0:7]
            desc = desc[9:]

        term: str = "description" if VALIDATION_MSG_LANGUAGE == "en" else "descricao"
        out_error[term] = desc
        result.append(out_error)

    return result


def __format_error(err_id: int, *args) -> str:

    err_msgs_en: Final[dict] = {
        10: "Value must be provided",
        11: "Invalid value {}",
        12: "Invalid value {}: length shorter than {}",
        13: "Invalid value {}: length longer than {}",
        14: "Invalid value {}: length must be {}",
        15: "Invalid value {}: must be {}",
        16: "Invalid value {}: must be one of {}",
        17: "Invalid value {}: must be in the range {}",
        18: "Invalid value {}: must be type {}",
        19: "Invalid value {}: date is later than the current date"
    }

    err_msgs_pt: Final[dict] = {
        10: "Valor deve ser fornecido",
        11: "Valor {} inválido",
        12: "Valor {} inválido: comprimento menor que {}",
        13: "Valor {} inválido: comprimento maior que {}",
        14: "Valor {} inválido: comprimento deve ser {}",
        15: "Valor {} inválido: deve ser {}",
        16: "Valor {} inválido: deve ser um de {}",
        17: "Valor {} inválido: deve estar no intervalo {}",
        18: "Valor {} inválido: deve ser do tipo {}",
        19: "Valor {} inválido: data posterior à data atual"
    }

    err_msgs: dict | None = None
    match VALIDATION_MSG_LANGUAGE:
        case "en":
            err_msgs = err_msgs_en
        case "pt":
            err_msgs = err_msgs_pt

    return validate_format_error(err_id, err_msgs, args)
