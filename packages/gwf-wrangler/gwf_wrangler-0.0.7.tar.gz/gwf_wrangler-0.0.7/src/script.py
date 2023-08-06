"""Convert yaml config files to LUA scripts"""
import json
import logging

from src.mapper import MAPPER_PROPS

logger = logging.getLogger(__name__)


class Script:
    """represents a dynamic lua script from yaml file"""

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return json.dumps(self.data, indent=4)

    def __iter__(self):
        return (x for x in self.data.items())

    def __getattr__(self, name):
        return self.data.get(name, None)

    def get_as_lua(self, key):
        """return keys value as Lua command"""
        results = []
        try:
            for item in self.data:
                results.extend(list(MAPPER_PROPS[key](item.get(key, None))))
            return results
        except AttributeError:
            return results


def find_script(name: str, scripts: list[Script]) -> Script:
    """returns common script if it exists"""
    try:
        return list(filter(lambda x: x.name == name, scripts))[0]
    except IndexError as err:
        raise ScriptNotFound(f"script {name} not found") from err


class ScriptNotFound(Exception):
    """Raised when a script name is not found"""
