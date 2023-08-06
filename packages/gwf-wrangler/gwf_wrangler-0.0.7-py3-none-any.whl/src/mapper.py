""" Maps Yaml Categories to functions to convert them to 
their YAML equivalents"""

import itertools
import os
from typing import Any


def ensure_list(value):
    """ensures a value is a list or coerces to list of len 1"""
    return value if isinstance(value, list) else [value]


def environment(values: list[dict[str, Any]]) -> list[str]:
    """returns list of EnvVariables"""
    results = []
    if not values:
        return results
    for value in ensure_list(values):
        for key, value in value.items():
            results.append(f'setenv("{key}", "{value}")\n')
    return results


def modules(values: list[str]) -> list[str]:
    """returns list of Modules"""
    results = []
    if not values:
        return results
    for value in ensure_list(values):
        key, _value = value.split("/")
        results.append(f'load(pathJoin("{key}", "{os.getenv(_value[2: -1])}"))\n')
    return results


def module_paths(values: list[str]) -> list[str]:
    """returns list of PosixPaths"""
    if not values:
        return []
    return [
        f'prepend_path("MODULEPATH", pathJoin("{_path}"))\n'
        for _path in values
        if _path != "None"
    ]


def what_is(values: list[str]) -> list[str]:
    """returns list of WhatIs"""
    if not values:
        return []
    return [f'whatis("{value}")\n' for value in ensure_list(values)]


def _help(values: list[str]) -> list[str]:
    """returns list of Help"""
    if not values:
        return []
    return [f"help([[{value}]])\n" for value in ensure_list(values)]


def extra(value: list[dict[str, Any]]):
    """converts extra dicts"""
    if not value:
        return []
    results = []
    for item in value:
        for key, _value in item.items():
            results.extend(itertools.chain(MAPPER_PROPS[key](ensure_list(_value))))
    return results


MAPPER_PROPS = {
    "modules": modules,
    "modulepaths": module_paths,
    "environment": environment,
    "whatis": what_is,
    "help": _help,
    "^extra": extra,
}
