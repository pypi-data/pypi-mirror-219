import json
from typing import Any

from frinx.common.type_aliases import DictAny


def jsonify_description(
    description: str, labels: list[str] | None = None, rbac: list[str] | None = None
) -> str:
    """Returns description in format of stringified JSON.
    >>> jsonify_description("Hello world")
    '{"description": "Hello world"}'
    >>> jsonify_description("Hello world", labels=["A", "B"])
    '{"description": "Hello world", "labels": ["A", "B"]}'
    >>> jsonify_description("Hello world", labels=["A", "B"], rbac=["C", "D"])
    '{"description": "Hello world", "labels": ["A", "B"], "rbac": ["C", "D"]}'
    """
    desc_representation: dict[str, Any] = {'description': description}
    if labels:
        desc_representation['labels'] = labels
    if rbac:
        desc_representation['rbac'] = rbac
    output = json.dumps(desc_representation)
    return output


def snake_to_camel_case(string: str) -> str:
    """Returns camelCase version of provided snake_case StrictString."""
    if not string:
        return ''

    words = string.split('_')
    result = words[0].lower() + ''.join(n.capitalize() for n in words[1:])
    return result


def normalize_base_url(url: str) -> str:
    return url.removesuffix('/')


def remove_empty_elements_from_dict(any_dict: DictAny) -> DictAny:
    return dict((k, v) for k, v in any_dict.items() if v)
