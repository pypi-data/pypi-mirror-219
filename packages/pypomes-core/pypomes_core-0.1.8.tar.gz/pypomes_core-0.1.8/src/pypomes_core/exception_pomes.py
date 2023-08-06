from types import TracebackType
from typing import Type
import os
import traceback


def exc_format(exc: Exception, exc_info: tuple[Type[BaseException], BaseException, TracebackType]) -> str:
    """
    Formata a mensagem de erro decorrente da exceção levantada em tempo de execução, no formato:

    <python_module>, <line_number>: <exc_class> - <exc_text>

    :param exc: a exceção levantada
    :param exc_info: informações associadas à exceção
    :return: a mensagem de erro formatada
    """
    tback: TracebackType = exc_info[2]
    cls: str = str(exc.__class__)

    # obtem o ponto de execução que provocou a exceção (última posição na pilha)
    tlast: traceback = tback
    while tlast.tb_next is not None:
        tlast = tlast.tb_next

    # obtem nome do módulo e linha do código (origem da exceção)
    try:
        fname: str = os.path.split(tlast.tb_frame.f_code.co_filename)[1]
    except Exception:
        fname: str = "<unknow module>"
    fline: int = tlast.tb_lineno
    return f"{fname}, {fline}, {cls[8:-2]} - {exc}"
