# -*- coding: utf-8 -*-
import operator
import os
import re
from functools import reduce

import configparser
from pybuilder.core import init

__author__ = u"Martin Grůber"

try:
    string_types = basestring
except NameError:
    string_types = str


def read_from(filename):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)) as f:
        result = f.read()
    return result


@init
def init_setup_cfg_plugin(project, logger):
    pass


@init
def init1_from_setup_cfg(project, logger):

    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    logger.debug(f"setup_cfg plugin: Project basedir: {project.basedir}")
    setup_filename = os.path.join(project.basedir, "setup.cfg")
    try:
        config.read(setup_filename)
    except Exception:
        logger.error(f"setup_cfg plugin: setup.cfg not loaded ({setup_filename})")
    else:
        logger.info(f"setup_cfg plugin: Loaded configuration from {setup_filename}")

    name = os.environ.get("PYB_SCFG_NAME", config.get("metadata", "name", fallback=None))
    version = os.environ.get("PYB_SCFG_VERSION", config.get("metadata", "version", fallback=None))
    if version and version.startswith("file: "):
        version = read_from(version.split(maxsplit=1)[1])
    distutils_commands = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), os.environ.get(
            "PYB_SCFG_DISTUTILS_COMMANDS", config.get("tool:pybuilder", "distutils_commands", fallback="sdist")
        ).split()
    )))
    distutils_upload_repository = os.environ.get(
        "PYB_SCFG_UPLOAD_REPOSITORY", config.get("tool:pybuilder", "distutils_upload_repository", fallback=None)
    )
    copy_resources_glob = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), config.get("tool:pybuilder", "copy_resources_glob", fallback="").split()
    )))

    package_data_tuples = [
        line.strip().split("=", maxsplit=1)
        for line in config.get("files", "package_data", fallback="").splitlines()
        if line.strip()
    ]
    if not package_data_tuples and config.has_section("options.package_data"):
        package_data_tuples = config.items("options.package_data")
    package_data = dict(map(
        lambda t: (t[0].strip(), re.split(r"\s|,\s*", t[1].strip())),
        package_data_tuples
    ))

    cython_include_modules = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), config.get("tool:pybuilder", "cython_include_modules", fallback="").split()
    )))
    cython_exclude_modules = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), config.get("tool:pybuilder", "cython_exclude_modules", fallback="").split()
    )))
    cython_remove_python_sources = config.getboolean(
        "tool:pybuilder", "cython_remove_python_sources", fallback=False
    )
    if config.has_section("tool:pybuilder.cython_compiler_directives"):
        cython_compiler_directives = dict(config.items("tool:pybuilder.cython_compiler_directives"))
    else:
        cython_compiler_directives = {}

    coverage_break_build_from_cfg = config.get("coverage:report", "fail_under", fallback=None)
    if coverage_break_build_from_cfg is None:
        coverage_break_build_from_cfg = config.get("tool:pytest", "coverage_break_build_threshold", fallback=None)
    pytest_coverage_break_build_threshold = os.environ.get(
        "PYB_SCFG_PYTEST_COVERAGE_BREAK_BUILD_THRESHOLD",
        coverage_break_build_from_cfg
    )

    pytest_coverage_html = config.getboolean("tool:pytest", "coverage_html", fallback=False)
    pytest_coverage_annotate = config.getboolean("tool:pytest", "coverage_annotate", fallback=False)

    scm_ver_version_scheme = config.get("tool:setuptools_scm", "version_scheme", fallback=None)
    scm_ver_version_scheme = os.environ.get("PYB_SCFG_SCM_VERSION_SCHEME", scm_ver_version_scheme)
    scm_ver_local_scheme = config.get("tool:setuptools_scm", "local_scheme", fallback=None)
    scm_ver_local_scheme = os.environ.get("PYB_SCFG_SCM_VERSION_SCHEME", scm_ver_local_scheme)
    scm_ver_root = config.get("tool:setuptools_scm", "root", fallback=None)
    scm_ver_root = os.environ.get("PYB_SCFG_SCM_ROOT", scm_ver_root)
    scm_ver_relative_to = config.get("tool:setuptools_scm", "relative_to", fallback=None)
    scm_ver_relative_to = os.environ.get("PYB_SCFG_SCM_RELATIVE_TO", scm_ver_relative_to)

    # analyze - Python flake8 linting
    # publish - create distributions (sdist, bdist)
    # upload - upload to the PyPI server
    # clean - clean all temporary files
    # sphinx_generate_documentation - generate sphinx documentation
    default_task = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), os.environ.get(
            "PYB_SCFG_DEFAULT_TASK", config.get("tool:pybuilder", "default_task", fallback="analyze publish clean")
        ).split()
    )))

    if name:
        project.set_property("name", name)
        # Setting property is not enough
        project.name = name
        logger.debug("setup_cfg plugin: Name set to: {}".format(name))

    if version:
        project.set_property("version", version)
        # Setting property is not enough
        project.version = project.get_property("version")
        logger.debug("setup_cfg plugin: Version set to: {}".format(version))

    if default_task:
        # Setting property is breaking this thing...
        # project.set_property("default_task", default_task)
        project.default_task = default_task
        logger.debug("setup_cfg plugin: Default task set to: {}".format(default_task))

    if distutils_commands:
        project.set_property_if_unset("distutils_commands", distutils_commands)
        logger.debug("setup_cfg plugin: Distutils commands set to: {}".format(distutils_commands))

    # TWINE_REPOSITORY_URL environment variable is preferred
    if os.environ.get("TWINE_REPOSITORY_URL") is None and distutils_upload_repository is not None:
        project.set_property_if_unset("distutils_upload_repository", distutils_upload_repository)
        logger.debug("setup_cfg plugin: Upload repository set to: {}".format(distutils_upload_repository))

    if len(cython_include_modules):
        # Cython extension modules definition
        project.set_property_if_unset("distutils_cython_ext_modules", [{
            "module_list": cython_include_modules,
            "exclude": cython_exclude_modules,
        }])
        logger.debug("setup_cfg plugin: Included cython modules: {}".format(cython_include_modules))
        logger.debug("setup_cfg plugin: Excluded cython modules: {}".format(cython_exclude_modules))

    if cython_remove_python_sources:
        # Remove the original Python source files from the distribution
        project.set_property_if_unset("distutils_cython_remove_python_sources", cython_remove_python_sources)
        logger.debug("setup_cfg plugin: Remove python sources when cythonized: {}".format(cython_remove_python_sources))
    if cython_compiler_directives:
        project.set_property_if_unset("distutils_cython_compiler_directives", cython_compiler_directives)
        logger.debug("setup_cfg plugin: Set cython compiler directives: {}".format(cython_compiler_directives))
    if copy_resources_glob:
        package_data.values()
        # Make the full files paths from the package name and the pattern; replace '.' in the package name with '/'
        package_data_patterns = [["/".join([k.replace(".", "/"), vi]) for vi in v] for k, v in package_data.items()]
        logger.debug(f"setup_cfg plugin: package_data_patterns: {package_data_patterns}")
        project.set_property_if_unset("copy_resources_glob", copy_resources_glob + reduce(
            operator.concat, package_data_patterns, [])
         )
        logger.debug(f"setup_cfg plugin: Configured resource copying glob: {copy_resources_glob}")

    if package_data:
        project.package_data.update(package_data.items())
        logger.debug("setup_cfg plugin: Added some package data")

    try:
        pytest_coverage_break_build_threshold = int(pytest_coverage_break_build_threshold)
    except (ValueError, TypeError):
        pytest_coverage_break_build_threshold = None
    if pytest_coverage_break_build_threshold is not None:
        project.set_property_if_unset("pytest_coverage_break_build_threshold", pytest_coverage_break_build_threshold)
        logger.debug("setup_cfg plugin: PyTest coverage break threshold set to {}".format(pytest_coverage_break_build_threshold))

    if scm_ver_version_scheme:
        project.set_property_if_unset("scm_ver_version_scheme", scm_ver_version_scheme)
        logger.debug("setup_cfg plugin: SCM version_scheme set to {}".format(scm_ver_version_scheme))

    if scm_ver_local_scheme:
        project.set_property_if_unset("scm_ver_local_scheme", scm_ver_local_scheme)
        logger.debug("setup_cfg plugin: SCM local_scheme set to {}".format(scm_ver_local_scheme))

    if scm_ver_root:
        project.set_property_if_unset("scm_ver_root", scm_ver_root)
        logger.debug("setup_cfg plugin: SCM root set to {}".format(scm_ver_root))

    if scm_ver_relative_to:
        project.set_property_if_unset("scm_ver_relative_to", scm_ver_relative_to)
        logger.debug("setup_cfg plugin: SCM relative_to set to {}".format(scm_ver_relative_to))

    project.set_property_if_unset("pytest_coverage_html", pytest_coverage_html)
    logger.debug("setup_cfg plugin: PyTest coverage HTML set to {}".format(pytest_coverage_html))

    project.set_property_if_unset("pytest_coverage_annotate", pytest_coverage_annotate)
    logger.debug("setup_cfg plugin: PyTest coverage annotateL set to {}".format(pytest_coverage_annotate))
