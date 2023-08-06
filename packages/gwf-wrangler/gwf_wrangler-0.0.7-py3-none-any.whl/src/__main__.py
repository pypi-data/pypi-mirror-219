"""main execution"""

import itertools
import logging
from pathlib import Path
from typing import Generator, Tuple

import yaml
from src.cli import get_cli_input

from src.script import Script, ScriptNotFound, find_script

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    # filename="wrangler.log",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

KEYWORD_INDICATOR = "^"


def load_scripts_from_yamls(_paths: list[Path]) -> Generator[list[Script], None, None]:
    """instantiates Script instances from yaml files"""
    for _path in _paths:
        logging.info("loading %s", _path)
        with open(_path, "r", encoding="utf-8") as _file:
            yield (
                [Script(name, data) for (name, data) in yaml.safe_load(_file).items()]
            )


def get_prepend_script(scripts):
    """returns the lua content of a prepend script if it exists"""
    try:
        return get_content(find_script("^pre", scripts))
    except ScriptNotFound:
        return []


def get_postpend_script(scripts):
    """returns the lua content of a postpend script if it exists"""
    try:
        return get_content(find_script("^post", scripts))
    except ScriptNotFound:
        return []


def get_bookend_scripts_content(scripts: list[Script]) -> Tuple[list[str], ...]:
    """returns the prepend and postpend scripts if thy exist"""
    return (get_prepend_script(scripts), get_postpend_script(scripts))


def get_content(_script: Script) -> list[str]:
    """returns the main content of a Script as Lua

    The content excludes anything not in the list below as they need to be
    treated differently with respect to parsing and ordering.

    * modulepaths
    * modules
    * environment
    """
    return list(
        itertools.chain(
            *[_script.get_as_lua(x) for x in ("modulepaths", "modules", "environment")]
        )
    )


def write_script_to_lua(
    output_path: Path,
    prepend_script: list[str],
    postpend_script: list[str],
    script: Script,
):
    """writes the script to file with bookend script contents

    This method is responsible for preserving the necessary order in which
    each YAML file is parsed, converted to Lua, and written to disk and is
    done so explicitly.
    """
    with open(
        Path(output_path / Path(f"{script.name}.lua")), "w", encoding="utf-8"
    ) as _output:
        _output.writelines(script.get_as_lua("help"))
        _output.writelines(prepend_script)
        _output.writelines(script.get_as_lua("modulepaths"))
        _output.writelines(script.get_as_lua("modules"))
        _output.writelines(script.get_as_lua("environment"))
        _output.writelines(postpend_script)
        _output.writelines(script.get_as_lua("^extra"))
        _output.writelines(script.get_as_lua("whatis"))


def scripts_to_process(scripts) -> list[Script]:
    """returns list of scripts to process excluding those
    denoted with a special character"""
    return [x for x in scripts if KEYWORD_INDICATOR not in x.name]


def process_scripts(output_path, scripts):
    """converts Script instances to Lua commands and writes output"""
    prepend_script, postpend_script = get_bookend_scripts_content(scripts)
    for script in scripts_to_process(scripts):
        write_script_to_lua(output_path, prepend_script, postpend_script, script)


def main():
    """main execution"""
    data = get_cli_input()
    _input: list[Path] = data["queue"]
    logger.debug("_input: %s", _input)
    output_path: Path = data["output_path"]
    logger.info("output path is %s", output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    for scripts in load_scripts_from_yamls(_input):
        process_scripts(output_path, scripts)


if __name__ == "__main__":
    main()
