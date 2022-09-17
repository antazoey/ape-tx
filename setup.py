#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup  # type: ignore

extras_require = {
    "test": [  # `test` GitHub Action jobs uses this
        "pytest>=7.0",  # Core testing package
        "pytest-xdist",  # multi-process runner
        "pytest-cov",  # Coverage analyzer plugin
        "hypothesis>=6.2.0,<7.0",  # Strategy-based fuzzer
        "ape-vyper",
    ],
    "lint": [
        "black>=22.6.0",  # auto-formatter and linter
        "mypy>=0.971",  # Static type analyzer
        "flake8>=4.0.1",  # Style linter
        "isort>=5.10.1",  # Import sorting linter
    ],
    "release": [  # `release` GitHub Action job uses this
        "setuptools",  # Installation tool
        "wheel",  # Packaging tool
        "twine",  # Package upload tool
    ],
    "dev": [
        "commitizen",  # Manage commits and publishing releases
        "pre-commit",  # Ensure that linters are run prior to commiting
        "pytest-watch",  # `ptw` test watcher/runner
        "IPython",  # Console for interacting
        "ipdb",  # Debugger (Must use `export PYTHONBREAKPOINT=ipdb.set_trace`)
    ],
}

# NOTE: `pip install -e .[dev]` to install package
extras_require["dev"] = (
    extras_require["test"]
    + extras_require["lint"]
    + extras_require["release"]
    + extras_require["dev"]
)

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="ape-tx",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="""ape-tx: transact from the command line""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juliya Smith",
    author_email="juliya@juliyasmith.com",
    url="https://github.com/unparallaled-js/ape-tx",
    include_package_data=True,
    install_requires=[
        "eth-ape>=0.5.1,<0.6",
        "click",  # Use same version as ape
    ],
    python_requires=">=3.8,<3.11",
    extras_require=extras_require,
    py_modules=["ape_tx"],
    entry_points={
        "ape_cli_subcommands": [
            "ape_tx=ape_tx._cli:cli",
        ],
    },
    license="Apache-2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"ape_tx": ["py.typed"]},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
