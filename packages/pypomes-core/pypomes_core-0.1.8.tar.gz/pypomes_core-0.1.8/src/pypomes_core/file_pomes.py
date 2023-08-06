from flask import Request
from werkzeug.datastructures import FileStorage


def file_from_request(request: Request, file_name: str = None, file_seq: int = 0) -> bytes:

    # inicializa a variável de retorno
    result: bytes | None = None

    count: int = len(request.files)
    # algum arquivo foi encontrado ?
    if count > 0:
        # sim, obtenha o arquivo
        file: FileStorage | None = None
        if isinstance(file_name, str):
            file = request.files.get(file_name)
        elif isinstance(file_seq, int) and file_seq >= 0:
            file_in: str = list(request.files)[file_seq]
            file = request.files[file_in]

        if file is not None:
            result: bytes = file.stream.read()

    return result
