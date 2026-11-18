"""Validação dos contratos de dados; não classifica risco nem decide execução."""
from __future__ import annotations

import math
import re


def validate_schema(value, schema, path='$'):
    """Valida o subconjunto JSON Schema usado pelos esquemas deste projeto.

    Não é um validador geral JSON Schema. Falha se o esquema introduzir uma
    palavra-chave não suportada, evitando ignorar silenciosamente restrições.
    """
    supported = {'$schema', 'title', 'description', 'type', 'const', 'enum',
                 'properties', 'required', 'additionalProperties', 'items',
                 'minimum', 'maximum', 'minLength', 'maxLength', 'pattern', 'oneOf'}
    unsupported = set(schema) - supported
    if unsupported:
        raise ValueError(f'{path}: palavra-chave de esquema não suportada: {sorted(unsupported)}')
    if 'oneOf' in schema:
        matches = 0
        for candidate in schema['oneOf']:
            try:
                validate_schema(value, candidate, path)
            except ValueError:
                continue
            matches += 1
        if matches != 1:
            raise ValueError(f'{path}: deve corresponder a exatamente uma assinatura')
    kinds = schema.get('type', [])
    kinds = [kinds] if isinstance(kinds, str) else kinds
    checks = {
        'object': lambda: type(value) is dict,
        'array': lambda: type(value) is list,
        'string': lambda: type(value) is str,
        'integer': lambda: type(value) is int,
        'number': lambda: type(value) in (int, float) and (type(value) is int or math.isfinite(value)),
        'boolean': lambda: type(value) is bool,
        'null': lambda: value is None,
    }
    if any(kind not in checks for kind in kinds):
        raise ValueError(f'{path}: tipo desconhecido no esquema')
    if kinds and not any(checks[kind]() for kind in kinds):
        raise ValueError(f'{path}: tipo ou número inválido; esperado {kinds}')
    if 'const' in schema and value != schema['const']:
        raise ValueError(f'{path}: versão ou constante inválida')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{path}: opção fora do enum')
    if type(value) is dict:
        missing = set(schema.get('required', [])) - set(value)
        if missing:
            raise ValueError(f'{path}: campos ausentes: {sorted(missing)}')
        properties = schema.get('properties', {})
        extra = set(value) - set(properties)
        additional = schema.get('additionalProperties', True)
        if extra and additional is False:
            raise ValueError(f'{path}: campos extras: {sorted(extra)}')
        for key, item in value.items():
            if key in properties:
                validate_schema(item, properties[key], f'{path}.{key}')
            elif isinstance(additional, dict):
                validate_schema(item, additional, f'{path}.{key}')
    if type(value) is list and 'items' in schema:
        for index, item in enumerate(value):
            validate_schema(item, schema['items'], f'{path}[{index}]')
    if type(value) in (int, float):
        for key, compare in [('minimum', lambda n: value < n), ('maximum', lambda n: value > n)]:
            if key in schema and compare(schema[key]):
                raise ValueError(f'{path}: fora do intervalo')
    if type(value) is str:
        if len(value) < schema.get('minLength', 0) or len(value) > schema.get('maxLength', float('inf')):
            raise ValueError(f'{path}: comprimento inválido')
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            raise ValueError(f'{path}: formato inválido')


def validate_jev_request(request, schema):
    validate_schema(request, schema)
    # Assinaturas, listas e limites estão no esquema canônico, inclusive oneOf.
