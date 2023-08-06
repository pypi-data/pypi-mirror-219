from flask import Request
import inspect
import types


def dict_has_key_chain(source: dict, key_chain: list[str]) -> bool:
    """
    Indicate the existence of an element in *source* pointed to by the nested keys chain
    *[keys[0]: ... :keys[n]*. The path up to he last key in the chain must point to an existing element.
    A given key may indicate the element's position within a *list*, using the format *<key>[<pos>]*.

    :param source: The reference dict.
    :param key_chain: The nested keys chain.
    :return: Whether the element exists.
    """
    # initialize the return variable
    result: bool = False

    # define the parent el;ement
    parent: dict | None = None

    # does the key chain contain just 1 element ?
    if len(key_chain) == 1:
        # yes, use the provided dict
        parent = source

    # does the key chain contain more than 1 element ?
    elif len(key_chain) > 1:
        # yes, obtain the parent element of the last key in the chain
        parent = dict_get_value(source, key_chain[:-1])

    # is the parent element a dict ?
    if isinstance(parent, dict):
        # yes, proceed
        key = key_chain[-1]

        # is the element denoted by the last key in the chain a list ?
        if key[-1] == "]":
            # yes, recover it
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            key = key[:pos]
            child = parent.get(key)
            # success, if the element in question is a list with more than 'inx' elements
            result = isinstance(child, list) and len(child) > inx

        # success, if the parent element contains the last key in the chain
        else:
            result = key in parent

    return result


def dict_get_value(source: dict, key_chain: list[str]) -> any:
    """
    Obtain the value of the element in *source* pointed to by the nested keys chain *[keys[0]: ... :keys[n]*.
    The path up to the last key in the chain must point to an existing element.
    A given key may indicate the element's position within a *list*, using the format *<key>[<pos>]*.
    Return *None* if the sought after value is not found.
    Note that returning *None* might not be indicative of the absence of the element in *source*,
    since that element might exist therein with the value *None*. To determine whether this is the case,
    use the operation *dict_has_value*.

    :param source: o dict de referência
    :param key_chain: a cadeia de chaves
    :return: o valor obtido
    """
    # inicializa a variável de retorno
    result: any = source

    # percorre as chaves da cadeia
    for key in key_chain:

        # é possível prosseguir ?
        if not isinstance(result, dict):
            # não, encerre a operação
            result = None
            break

        # a chave denota um elemento de lista ?
        if key[-1] == "]":
            # sim, recupere-o
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            result = result.get(key[:pos])

            # é possível prosseguir ?
            if isinstance(result, list) and len(result) > inx:
                # sim, prossiga
                result = result[inx]
            else:
                # não, aborte a operação
                result = None
        else:
            # não, recupere o elemento 'key' do dicionário
            result = result.get(key)

    return result


def dict_set_value(target: dict, key_chain: list[str], value: any):
    """
    Atribui ao elemento de *source*, apontado pela cadeia de chaves aninhadas *[keys[0]: ... :keys[n]*,
    o valor *value*. Caso o elemento final não exista, será criado com o valor especificado.
    Os elementos intermediários, caso não existam, serão criados com o valor de um *dict* vazio.

    Uma chave pode indicar a posição do elemento dentro de uma lista, utilizando para tanto
    o formato *<key>[<pos>]*, e nesse caso, o elemento deve existir.

    :param target: o dict de referência
    :param key_chain: a cadeia de chaves
    :param value: o valor a ser atribuído ao elemento
    """
    dict_item: any = target
    # percorre a cadeia até a penúltima chave
    for key in key_chain[:-1]:

        # é possível prosseguir ?
        if not isinstance(dict_item, dict):
            # não, aborte a operação
            break

        # a chave denota um elemento de lista ?
        if key[-1] == "]":
            # sim, recupere-o
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            dict_item = dict_item.get(key[:pos])
            # é possível prosseguir ?
            if isinstance(dict_item, list) and len(dict_item) > inx:
                # sim, prossiga
                dict_item = dict_item[inx]
            else:
                # não aborte a operação
                dict_item = None
        else:
            # não, dict_item tem a chave como elemento ?
            if key not in dict_item:
                # não, atribua a dict_item a chave com valor de um dicionário vazio
                dict_item[key] = {}
            dict_item = dict_item.get(key)

    # existe chave e dict_item é um dicionário ?
    if len(key_chain) > 0 and isinstance(dict_item, dict):
        # sim, prossiga
        key: str = key_chain[-1]
        # a chave denota um elemento de lista ?
        if key[-1] == "]":
            # sim, recupere-o
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            dict_item = dict_item.get(key[:pos])
            # a atribuição é possível ?
            if isinstance(dict_item, list) and len(dict_item) > inx:
                # sim, faça-a
                dict_item[inx] = value
        else:
            # não, faça a atribuição ao elemento 'key' do dicionário
            dict_item[key] = value


def dict_pop_value(target: dict, key_chain: list[str]) -> any:
    """
    Remove e retorna o valor do elemento de *source* apontado pela cadeia de chaves aninhadas
    *[keys[0]: ... :keys[n]*. O caminho até a última chave deve apontar para elementos existentes.
    Uma chave pode indicar a posição do elemento dentro de uma lista, utilizando para tanto
    o formato *<key>[<pos>]*. Retorna *None* se o valor procurado não for encontrado.

    Note que o retorno do valor *None* pode não ser indicativo da ausência do elemento em *source*, quando
    da invocaçxão dessa operação, uma vez que esse elemento pode ter existido com o próprio valor *None*.
    Para certificar-se disso, use antes a operação *dict_has_value*.

    :param target: o dict de referência
    :param key_chain: a cadeia de chaves
    :return: o valor removido
    """
    # inicializa a variável de retorno
    result: any = None

    # obtem o elemento pai do elemento denotado pela última chave da cadeia
    parent: dict | None = None

    # a cadeia de chaves contem 1 único elemento ?
    if len(key_chain) == 1:
        # sim, utilize o dict fornecido
        parent = target

    # a cadeia de chaves contem mais de 1 elemento ?
    elif len(key_chain) > 1:
        # sim, obtenha o elemento pai da última chave da cadeia
        parent = dict_get_value(target, key_chain[:-1])

    # o elemento pai é um dicionário ?
    if isinstance(parent, dict):
        # sim, prossiga
        key: str = key_chain[-1]

        # a última chave da cadeia denota um elemento de lista ?
        if key[-1] == "]":
            # sim, recupere a lista em questão
            pos: int = key.find("[")
            inx: int = int(key[pos+1:-1])
            key = key[:pos]
            child: any = parent.get(key)

            #  o elemento da última chave da cadeia é uma lista com mais de 'inx' elementos ?
            if isinstance(child, list) and len(child) > inx:
                # sim, remova o elemento indicado e retorne seu valor
                result = child.pop(inx)

        # o item pai contem a última chave da cadeia ?
        elif key in parent:
            # sim, remova o elemento indicado e retorne seu valor
            result = parent.pop(key)

    return result


def dict_replace_value(target: dict, old_value: any, new_value: any):
    """
    Substitui em *target* todas as ocorrências de *old_value* por *new_value*.

    :param target: o dict de referência
    :param old_value: o valor a ser substituído
    :param new_value: o novo valor
    """
    def list_replace_value(items: list[any], old_val: any, new_val: any):
        # percorre a lista
        for item in items:

            # o item é um dicionário ?
            if isinstance(item, dict):
                # sim, processe-o recursivamente
                dict_replace_value(item, old_val, new_val)

            # o item é uma lista ?
            elif isinstance(item, list):
                # sim, processe-o recursivamente
                list_replace_value(item, old_val, new_val)

    # percorre o dicionário
    for curr_key, curr_value in target.items():

        # o valor atual é o valor buscado ?
        if curr_value == old_value:
            # sim, substitua-o
            target[curr_key] = new_value

        # o valor atual é um dicionário ?
        elif isinstance(curr_value, dict):
            # sim, processe-o recursivamente
            dict_replace_value(curr_value, old_value, new_value)

        # o valor atual é uma lista ?
        elif isinstance(curr_value, list):
            # sim, processe-o recursivamente
            list_replace_value(curr_value, old_value, new_value)


def dict_get_key(source: dict, value: any) -> any:
    """
    Retorna a chave em *source*, associada à primeira ocorrência de *value* encontrada,
    ou *None*, se nenhuma chave for encontrada. Apenas os atributos no primeiro nível
    em *source* são inspecionados.

    :param source: dicionário a ser pesquisado
    :param value: valor de referência
    :return: primeira chave associada ao valor de referência
    """
    result: any = None
    for key, val in source.items():
        if val == value:
            result = key
            break

    return result


def dict_get_keys(source: dict, value: any) -> list[str]:
    """
    Restorna lista com todas as chaves ne primeiro nível em *source*, associadas a *value*,
    ou *[]* se nenhuma chave for encontrada.

    :param source: dicionário a ser pesquisado
    :param value: valor de referência
    :return: lista de chaves associadas ao valor de referência
    """
    return [key for key, val in source.items() if val == value]


def dict_merge(target: dict, source: dict):
    """
    Percorre os elementos de *source* para atualizar *target*, obedecendo aos seguintes os critérios:

    - acrescentar o elemento a *target*, se não existir
    - se o elemento existir em *target*:

      -   processar recursivamente os dois elementos, se ambos forem do tipo *dict*
      -   acrescentar os itens faltantes, se ambos forem do tipo *list*
      -   substituir o elemento em *target* se for de outro tipo, ou se os tipos forem diferentes entre si

    :param target: o dicionário a ser atualizado
    :param source: o dicionário com os novos elementos
    """
    # percorre o dicionário com os novos elementos
    for skey, svalue in source.items():

        # o item existe em target ?
        if skey in target:
            # sim, prossiga
            tvalue: any = target.get(skey)

            # ambos os elementos são dicionários ?
            if isinstance(svalue, dict) and isinstance(tvalue, dict):
                # sim, processe-os recursivamente
                dict_merge(tvalue, svalue)

            # ambos os elementos são listas ?
            elif isinstance(svalue, list) and isinstance(tvalue, list):
                # sim, acrescente os elementos faltantes
                for item in svalue:
                    if item not in tvalue:
                        tvalue.append(item)
            else:
                # os elementos não são ambos listas ou dicionários, substitua o valor em target
                target[skey] = svalue
        else:
            # não, acrescente-o
            target[skey] = svalue


def dict_coalesce(target: dict, key_chain: list[str]):
    """
    Coalesce o elemento do tipo *list* em *target* no nível *n*, apontado pela cadeia de
    chaves aninhadas *[keys[0]: ... :keys[n]*, com a lista no nível imediatamente anterior,
    como uma sequência de multiplos elementos. Para tanto, as duas últimas chaves da cadeia
    *key_chain* devem estar associadas a valores do tipo *list*.

    :param target: o dicionário a ser coalescido
    :param key_chain: a cadeia de chaves
    """
    # a cadeia de chaves contem mais de 2 chaves ?
    if len(key_chain) > 2:
        # sim, prossiga

        curr_dict: dict | None = target
        # percorre a cadeia até a antepenúltima chave
        for inx, key in enumerate(key_chain[:-2]):

            # é possível prosseguir ?
            if not isinstance(curr_dict, dict):
                # não, aborte a operação
                break

            # key está associado a uma lista ?
            in_list: list[any] = curr_dict.get(key)
            if isinstance(in_list, list):
                # sim, invoque recursivamente o coalescimento dos dicionários da lista
                for in_dict in in_list:
                    # o item da lista é um dicionário ?
                    if isinstance(in_dict, dict):
                        # sim, coalesça-o recursivamente
                        dict_coalesce(in_dict, key_chain[inx + 1:])
                # termina a operação
                curr_dict = None
                break
            else:
                # não, prossiga com o valor associado a key
                curr_dict = curr_dict.get(key)

        # curr_dict é um dicionário contendo a penúltima chave ?
        if isinstance(curr_dict, dict) and \
           isinstance(curr_dict.get(key_chain[-2]), list):
            # sim, prossiga com o coalescimento
            penultimate_elem: list[dict] = curr_dict.pop(key_chain[-2])
            penultimate_list: list[dict] = []

            # percorre os items do penúltimo elemento
            for last_elem in penultimate_elem:

                # last_elem é um dicionário ?
                if isinstance(last_elem, dict):
                    # sim, prossiga
                    outer_dict: dict = {}
                    last_list: list[dict] = []

                    # percorre os itens de last_elem
                    for k1, v1 in last_elem.items():
                        # a chave é a última chave e está associada a uma lista ?
                        if k1 == key_chain[-1] and isinstance(v1, list):
                            # sim, obtenha seus itens para coalescimento posterior
                            for in_dict in v1:
                                # in_dict é um dicionário ?
                                if isinstance(in_dict, dict):
                                    # sim, salve-o coalescido
                                    inner_dict: dict = {}
                                    for k2, v2 in in_dict.items():
                                        inner_dict[k2] = v2
                                    last_list.append(inner_dict)
                                else:
                                    # não, salve-o como está
                                    last_list.append(in_dict)
                        else:
                            # não, coalesça esse item
                            outer_dict[k1] = v1

                    # há itens para coalescimento ?
                    if len(last_list) > 0:
                        # sim, coalesça-os
                        for in_dict in last_list:
                            # in_dict é um dicionário ?
                            if isinstance(in_dict, dict):
                                # sim, acrescente a ele os dados já salvos
                                in_dict.update(outer_dict)
                            # salva o item
                            penultimate_list.append(in_dict)
                    else:
                        # não, salve os itens já coalescidos
                        penultimate_list.append(outer_dict)
                else:
                    # não, salve-o
                    penultimate_list.append(last_elem)

            # substitue a lista original associada à penúltima chave com a nova lista coalescida
            curr_dict[key_chain[-2]] = penultimate_list


def dict_reduce(target: dict, key_chain: list[str]):
    """
    Realoca os elementos de *target* no nível *n*, apontados pela cadeia de chaves aninhadas
    *[keys[0]: ... :keys[n]*, para o nível imediatamente acima, e remove o elemento no nivel *n*
    ao final.

    :param target: o dicionário a ser reduzido
    :param key_chain: a cadeia de chaves
    """
    # a cadeia de chaves contem pelo menos 1 chave ?
    if len(key_chain) > 0:
        # sim, prossiga

        curr_dict: dict | None = target
        # percorre a cadeia até a penúltima chave
        for inx, key in enumerate(key_chain[:-1]):

            # é possível prosseguir ?
            if not isinstance(curr_dict, dict):
                # não, aborte a operação
                break

            # key está associado a uma lista ?
            in_list: list[any] = curr_dict.get(key)
            if isinstance(in_list, list):
                # sim, invoque recursivamente a redução dos dicionários da lista
                for in_dict in in_list:
                    # o item da lista é um dicionário ?
                    if isinstance(in_dict, dict):
                        # sim, reduza-o recursivamente
                        dict_reduce(in_dict, key_chain[inx + 1:])
                # termine a operação
                curr_dict = None
                break
            else:
                # não, prossiga com o valor associado a key
                curr_dict = curr_dict.get(key)

        last_key: str = key_chain[-1]
        # curr_dict contem um dicionário associado a last_key ?
        if isinstance(curr_dict, dict) and \
           isinstance(curr_dict.get(last_key), dict):
            # sim, prossiga com a redução
            last: dict = curr_dict.pop(last_key)
            for key, value in last.items():
                curr_dict[key] = value


def dict_from_list(source: list[dict], key_chain: list[str], value: any) -> dict:
    """
    Localiza em *source*, e retorna, o elemento do tipo *dict* contendo a cadeia de chaves
    *key_chain* com o valor *value*. Retorna *None* se esse *dict* não for encontrado.

    :param source: a lista a ser inspecionada
    :param key_chain: a cadeia de chaves usada na busca
    :param value: o valor associado à cadeia de chaves
    :return: o dict procurado
    """
    # inicializa a variável de retorno
    result: dict | None = None

    for item in source:
        if isinstance(item, dict) and \
           value == dict_get_value(item, key_chain):
            result = item
            break

    return result


def dict_from_object(source: object) -> dict:
    """
    Percorre *source* e cria um *dict* com seus atributos contendo valores não nulos. *source* pode ser
    qualquer objeto, especialmente aqueles que tenham sido decorados com *@dataclass*.

    :param source: o objeto de referência
    :return: dicionário com estrutura equivalente ao objeto de referência
    """
    # inicializa a variável de retorno
    result: dict = {}

    source_module: types.ModuleType = inspect.getmodule(source)
    source_dict: dict = source.__dict__
    for key, value in source_dict.items():
        # value é nulo ou lista vazia ?
        if not (value is None or (isinstance(value, list) and len(value) == 0)):
            # não, prossiga
            name: str = key

            # value é uma lista ?
            if isinstance(value, list):
                # sim, percorra-a
                result[name] = []
                for list_item in value:
                    # list_item é um objeto do mesmo módulo ?
                    if source_module == inspect.getmodule(list_item):
                        # sim, prossiga recursivamente
                        result[name].append(dict_from_object(list_item))
                    else:
                        # não, prossiga linearmente
                        result[name].append(list_item)

            # value é um objeto do mesmo módulo ?
            elif source_module == inspect.getmodule(value):
                # sim, prossiga recursivamente
                result[name] = dict_from_object(value)
            else:
                # não, prossiga linearmente
                result[name] = value

    return result


def dict_from_form(request: Request) -> dict:
    """
    Constrói e retorna um *dict* com os parâmetros encontrados no form existente em *request*.

    :param request: the HTTP request
    :return: dicionários contendo os parâmetros encontrados.
    """

    # inicializa variável de retorno
    result: dict = {}

    # percorre os parâmetros do form
    for key, value in request.form.items():
        result[key] = value

    return result


def dict_transform(source: dict, from_to_keys: list[tuple[str, str]],
                   prefix_from: str = None, prefix_to: str = None) -> dict:
    """
    Constrói um novo *dict*, atribuindo a cada elemento indicado pelo segundo elemento de uma
    tupla contendo uma cadeia de chaves aninhadas em *from_to_keys*, o valor do elemento
    de *source* indicado pelo primeiro elemento da tupla, também contendo uma cadeia de chaves
    aninhadas, respectivamente para todos os elementos mapeados em *from_to_keys*.

    Os prefixos para as chaves de origem e de destino, se definidos, tem tratamentos distintos.
    São acrescentados na busca de valores em *Source*, e removidos na atribuição de valores
    ao *dict* de retorno.

    :param source: o dict de origem dos valores
    :param from_to_keys: a lista de tuplas contendo as sequências de chaves de origem e destino
    :param prefix_from: prefixo a ser acrescentado às chaves de origem
    :param prefix_to: prefixo a ser removido das chaves de destino
    :return: o novo dicionário
    """
    # import the neeeded functions
    from .list_pomes import list_find_coupled, list_transform, list_unflatten

    # inicializa a variável de retorno
    result: dict = {}

    # percorre o dicionário de origem
    for key, value in source.items():

        # define a cadeia de chaves de origem
        if prefix_from is None:
            from_keys: str = key
        else:
            from_keys: str = f"{prefix_from}.{key}"

        # obtem a cadeia de chaves de destino
        to_keys: str = list_find_coupled(from_to_keys, from_keys)

        # o destino foi definido ?
        if to_keys is not None:
            # sim, obtenha o valor de destino
            if isinstance(value, dict):
                # valor é um dicionário, transforme-o
                to_value: dict = dict_transform(value, from_to_keys, from_keys, to_keys)
            elif isinstance(value, list):
                # valor é uma lista, transforme-a
                to_value: list = list_transform(value, from_to_keys, from_keys, to_keys)
            else:
                # valor não é dicionário ou lista
                to_value: any = value

            # o prefixo de destino foi definido e ocorre na cadeia de destino ?
            if prefix_to is not None and to_keys.startswith(prefix_to):
                # sim, remova o prefixo
                to_keys = to_keys[len(prefix_to)+1:]
            to_keys_deep: list[str] = list_unflatten(to_keys)

            # atribui o valor transformado ao resultado
            dict_set_value(result, to_keys_deep, to_value)

    return result


def dict_listify(target: dict, key_chain: list[str]):
    """
    Insere o valor do item de *target* apontado pela cadeia de chaves aninhadas
    *[keys[0]: ... :keys[n]* em uma lista, se esse valor já não for uma lista.
    Todas as listas eventualmente encontradas no percurso até a penúltima chava
    da cadeia serão recursivamente processadas.

    :param target: dicionário a ser modificado
    :param key_chain: cadeia de chaves aninhadas apontando para o item em questão
    """
    def items_listify(in_targets: list, in_keys: list[str]):

        # percorra os itens da lista
        for in_target in in_targets:
            # o elemento é um dicionário ?
            if isinstance(in_target, dict):
                # sim, processe-o
                dict_listify(in_target, in_keys)
            # o elemento é uma lista ?
            elif isinstance(in_target, list):
                # sim, processe-o recursivamente
                # (cadeia de chaves também se aplica a listas diretamente aninhadas em listas)
                items_listify(in_target, in_keys)

    parent: any = target
    # percorre a cadeia até a penúltima chave
    for inx, key in enumerate(key_chain[:-1]):
        parent = parent.get(key)
        # o item é uma lista ?
        if isinstance(parent, list):
            # sim, processe-o e encerre a operação
            items_listify(parent, key_chain[inx+1:])
            parent = None

        # é possível prosseguir ?
        if not isinstance(parent, dict):
            # não, aborte o loop
            break

    if isinstance(parent, dict) and len(key_chain) > 0:
        key: str = key_chain[-1]
        # o item existe e não é uma lista ?
        if key in parent and not isinstance(parent.get(key), list):
            # sim, insira-o em uma lista
            item: any = parent.pop(key)
            parent[key] = [item]


if __name__ == "__main__":

    s1 = {
        "a0": 0,
        "a1": {
            "b0": "qwert",
            "b1": {
                "c0": None,
                "c1": [1, {"d": [2, {"e": 3}, 4]}, {"d": 5}, {"d": [6, 7]}, [8, 9]]
            }
        }
    }
    mapping = [
        ("a0", "w0"),
        ("a1", "w1"),
        ("a1.b0", "w1.x0"),
        ("a1.b1", "w1.x1"),
        ("a1.b1.c0", "w1.x1.r.y0"),
        ("a1.b1.c1", "w1.x1.y1"),
        ("a1.b1.c1.d", "w1.x1.y1.z")
    ]
    s2 = dict_transform(s1, mapping)

    print(f"dict original:     {s1}")
    keys: list[str] = ["a1", "b1"]
    print(f"cadeia de redução: {keys}")
    dict_reduce(s1, keys)
    print(f"dict reduzido:     {s1}")
    keys = ["a1", "c1", "d"]
    print(f"cadeia para list.: {keys}")
    dict_listify(s1, keys)
    print(f"dict listificado:  {s1}")
    keys = ["a1", "c1", "d"]
    print(f"cadeia para coal.: {keys}")
    dict_coalesce(s1, keys)
    print(f"dict coalescido:   {s1}")
    print(f"mapeamento:        {mapping}")
    print(f"dict transformado: {s2}")
