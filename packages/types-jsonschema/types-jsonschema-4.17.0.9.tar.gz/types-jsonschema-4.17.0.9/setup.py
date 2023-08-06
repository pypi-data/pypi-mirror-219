from setuptools import setup

name = "types-jsonschema"
description = "Typing stubs for jsonschema"
long_description = '''
## Typing stubs for jsonschema

This is a PEP 561 type stub package for the `jsonschema` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`jsonschema`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/jsonschema. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `19257305853dc5fe0c5d7d248fe112b931f9244a` and was tested
with mypy 1.4.1, pyright 1.1.316, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="4.17.0.9",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/jsonschema.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['jsonschema-stubs'],
      package_data={'jsonschema-stubs': ['__init__.pyi', '_format.pyi', '_legacy_validators.pyi', '_types.pyi', '_utils.pyi', '_validators.pyi', 'cli.pyi', 'exceptions.pyi', 'protocols.pyi', 'validators.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
