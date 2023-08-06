#!/usr/bin/env python3
"""Generate an updated requirements_all.txt."""
import difflib
import importlib
import os
import pkgutil
import sys
from pathlib import Path

import packaging.requirements as pack_req

from .shc_from_manifests.integration import Integration
from .shc_from_manifests.requirements import normalize_package_name

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

IGNORE_PIN = ("colorlog>2.1,<3", "urllib3")

URL_PIN = (
    "https://developers.home-assistant.io/docs/" +
    "creating_platform_code_review.html#1-requirements"
)


CONSTRAINT_BASE = """
# Constrain pycryptodome to avoid vulnerability
# see https://github.com/home-assistant/core/pull/16238
pycryptodome>=3.6.6

# Constrain urllib3 to ensure we deal with CVE-2020-26137 and CVE-2021-33503
urllib3>=1.26.5

# Constrain httplib2 to protect against GHSA-93xj-8mrv-444m
# https://github.com/advisories/GHSA-93xj-8mrv-444m
httplib2>=0.19.0

# This is a old unmaintained library and is replaced with pycryptodome
pycrypto==1000000000.0.0

# This overrides a built-in Python package
enum34==1000000000.0.0
typing==1000000000.0.0
uuid==1000000000.0.0

# regex causes segfault with version 2021.8.27
# https://bitbucket.org/mrabarnett/mrab-regex/issues/421/2021827-results-in-fatal-python-error
# This is fixed in 2021.8.28
regex>=2021.8.28
"""


def explore_module(package, explore_children):
    """Explore the modules."""
    module = importlib.import_module(package)

    found = []

    if not hasattr(module, "__path__"):
        return found

    for _, name, _ in pkgutil.iter_modules(module.__path__, f"{package}."):
        found.append(name)

        if explore_children:
            found.extend(explore_module(name, False))

    return found


def core_requirements():
    """Gather core requirements out of pyproject.toml."""
    with open("pyproject.toml", "rb") as fp:
        data = tomllib.load(fp)
    reqs: list[str] = []
    for req in data["project"]["dependencies"]:
        try:
            parsed = pack_req.Requirement(req)
            name = normalize_package_name(req)
            if name != parsed.name:
                req = req.replace(parsed.name, name)
                parsed = pack_req.Requirement(req)
            reqs.append(str(parsed))
        except pack_req.InvalidRequirement:
            continue

    return reqs


def gather_recursive_requirements(domain, seen=None):
    """Recursively gather requirements from a module."""
    if seen is None:
        seen = set()

    if domain in seen:
        return {}

    seen.add(domain)
    integration = Integration(Path(f"smart_home_tng/components/{domain}"))
    integration.load_manifest()
    reqs = set()
    for req in integration.requirements:
        try:
            parsed = pack_req.Requirement(req)
            name = normalize_package_name(req)
            if parsed.name != name:
                req = req.replace(parsed.name, name)
                parsed = pack_req.Requirement(req)
            reqs.add(str(parsed))
        except pack_req.InvalidRequirement:
            pass
    for dep_domain in integration.dependencies:
        reqs.update(gather_recursive_requirements(dep_domain, seen))
    return reqs


def gather_modules():
    """Collect the information."""
    reqs = {}

    errors = []

    gather_requirements_from_manifests(errors, reqs)
    gather_requirements_from_modules(errors, reqs)

    for key in reqs:
        reqs[key] = sorted(reqs[key], key=lambda name: (len(name.split(".")), name))

    if errors:
        print("******* ERROR")
        print("Errors while importing: \n", "\n".join(errors))
        return None

    return reqs


def gather_requirements_from_manifests(errors, reqs):
    """Gather all of the requirements from manifests."""
    integrations = Integration.load_dir(Path("smart_home_tng/components"))
    for domain in sorted(integrations):
        integration = integrations[domain]

        if not integration.manifest:
            errors.append(f"The manifest for integration {domain} is invalid.")
            continue

        if integration.disabled:
            continue

        process_requirements(
            errors,
            integration.requirements,
            f"smart_home_tng.components.{domain}",
            reqs,
        )


def gather_requirements_from_modules(errors, reqs):
    """Collect the requirements from the modules directly."""
    for package in sorted(
        explore_module("smart_home_tng.scripts", True)
        + explore_module("smart_home_tng.auth", True)
    ):
        try:
            module = importlib.import_module(package)
        except ImportError as err:
            print(f"{package.replace('.', '/')}.py: {err}")
            errors.append(package)
            continue

        if getattr(module, "REQUIREMENTS", None):
            process_requirements(errors, module.REQUIREMENTS, package, reqs)


def process_requirements(errors, module_requirements, package, reqs):
    """Process all of the requirements."""
    for req in module_requirements:
        try:
            parsed = pack_req.Requirement(req)
        except pack_req.InvalidRequirement:
            errors.append(f"{package}[format of '{req}' is not valid.]")
            continue

        if parsed.url is not None:
            errors.append(f"{package}[Only pypi dependencies are allowed: {req}]")
        if (parsed.specifier is None) and (parsed.name not in IGNORE_PIN):
            errors.append(f"{package}[Please pin requirement {req}, see {URL_PIN}]")
        normalized_name = normalize_package_name(req)
        if parsed.name != normalized_name:
            req = req.replace(parsed.name, normalized_name)
            parsed = pack_req.Requirement(req)
        reqs.setdefault(str(parsed), []).append(package)


def gather_constraints():
    """Construct output for constraint file."""
    return (
        "\n".join(
            sorted(
                {
                    *core_requirements(),
                    *gather_recursive_requirements("default_config"),
                    *gather_recursive_requirements("mqtt"),
                }
            )
            + [""]
        )
        + CONSTRAINT_BASE
    )


def diff_file(filename, content):
    """Diff a file."""
    return list(
        difflib.context_diff(
            [f"{line}\n" for line in Path(filename).read_text(encoding="utf-8").split("\n")],
            [f"{line}\n" for line in content.split("\n")],
            filename,
            "generated",
        )
    )


def main(validate):
    """Run the script."""
    if not os.path.isfile("smart_home_tng/package_constraints.txt"):
        print("Run this from smart-home-tng root dir")
        return 1

    data = gather_modules()

    if data is None:
        return 1

    # reqs_file = requirements_output(data)
    # reqs_all_file = requirements_all_output(data)
    # reqs_test_all_file = requirements_test_all_output(data)
    # reqs_pre_commit_file = requirements_pre_commit_output()
    constraints = gather_constraints()

    files = (
        # ("requirements.txt", reqs_file),
        # ("requirements_all.txt", reqs_all_file),
        # ("requirements_test_pre_commit.txt", reqs_pre_commit_file),
        # ("requirements_test_all.txt", reqs_test_all_file),
        ("smart_home_tng/package_constraints.txt", constraints),
    )

    if validate:
        errors = []

        for filename, content in files:
            diff = diff_file(filename, content)
            if diff:
                errors.append("".join(diff))

        if errors:
            print("ERROR - FOUND THE FOLLOWING DIFFERENCES")
            print()
            print()
            print("\n\n".join(errors))
            print()
            print("Please run python3 -m script.gen_requirements_all")
            return 1

        return 0

    for filename, content in files:
        Path(filename).write_text(content)

    return 0


if __name__ == "__main__":
    _VAL = sys.argv[-1] == "validate"
    sys.exit(main(_VAL))
