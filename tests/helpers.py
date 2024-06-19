import json
import os
import logging
import re

import titan.resources as resources

from titan.resources import Resource
from titan.enums import ResourceType
from titan.parse import _split_statements


logger = logging.getLogger("titan")

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "../examples")


def _get_resource_cls(resource_name):
    resource_name = resource_name.replace("_", "")
    for resource_cls in Resource.__subclasses__():
        if resource_cls.__name__.lower() == resource_name:
            return resource_cls
    raise ValueError(f"Resource class {resource_name} not found")


def camelcase_to_snakecase(name: str) -> str:
    pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
    name = pattern.sub("_", name).lower()
    return name


def get_json_fixture(resource_name):
    with open(os.path.join(FIXTURES_DIR, "json", f"{resource_name}.json"), "r") as file:
        content = file.read()
        if not content:
            raise ValueError(f"Empty JSON fixture for {resource_name}")
        try:
            return json.loads(content)
        except Exception as err:
            raise ValueError(f"Failed to decode JSON for {resource_name}: {err}")


def get_json_fixtures():
    files = os.listdir(os.path.join(FIXTURES_DIR, "json"))
    for f in sorted(files):
        if f.endswith(".json"):
            resource_name = f.split(".")[0]
            try:
                resource_cls = _get_resource_cls(resource_name)
            except ValueError:
                continue
            try:
                data = get_json_fixture(resource_name)
                yield (resource_cls, data)
            except Exception:
                continue


def get_sql_fixtures():
    files = os.listdir(os.path.join(FIXTURES_DIR, "sql"))
    for f in sorted(files):
        if f.endswith(".sql"):
            resource_name = f.split(".")[0]
            try:
                resource_cls = _get_resource_cls(resource_name)
            except ValueError as err:
                logger.warning(f"SQL fixture file {f} has a problem: {err}")
                continue

            idx = 1
            for fixture in get_sql_fixture(f):
                yield (resource_cls, fixture, idx)
                idx += 1


def get_sql_fixture(filename, lines=False):
    with open(os.path.join(FIXTURES_DIR, "sql", filename), encoding="utf-8") as f:
        if lines:
            yield from f.read().splitlines()
        else:
            yield from _split_statements(f.read())


def get_examples_yml():
    for file_name in os.listdir(EXAMPLES_DIR):
        if file_name.endswith(".yml"):
            with open(os.path.join(EXAMPLES_DIR, file_name), "r") as file:
                yield (file_name[:-4], file.read())
