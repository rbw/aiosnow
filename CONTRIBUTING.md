# Contributing to the aiosnow project

aiosnow aims to have relaxed contribution requirements. They are listed below.

## Style

### Python

The code is expected to conform to *Black* and *PEP8*, and include type annotations. Tools are provided for linting and reformatting.

#### Lint

Checks if the code is correctly formatted, and that type annotations are in place.

```
$ make lint
```


#### Reformat

Formats code using *black*, *autoflake* and *isort*.

```
$ make reformat
```


### Git
- Use the present tense ("Add feature" not "Added feature")
- Limit the first line to 72 characters or less


### Documentation

- Docstrings should be written ins Google Style
- Sphinx docs should use reStructuredText

## Development tools

aiosnow uses Poetry for working with the project. Guides for its installation procedure is described over at [python-poetry/poetry](https://github.com/python-poetry/poetry#installation).

With poetry installed, run `make` in the project root for a list of available commands.

### Install

Creates a virtual environment and installs dependencies in *.poetry/*

```
$ make install
```

### Update

Updates dependencies in *.poetry/*

```
$ make update
```

### Shell

Activates the virtual environment.

```
$ make shell
```


### Test

Runs tests.

```
$ make test
```

#### Clean

Removes cache and bytecode files.

```
$ make clean
```

### Publish

Uploads aiosnow to PyPI.

```
$ make publish
```

