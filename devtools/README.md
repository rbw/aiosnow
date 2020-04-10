# Development tools

Snow uses Poetry for working with the project. Guides for its installation procedure is described at [python-poetry/poetry](https://github.com/python-poetry/poetry#installation).

With poetry installed, run `make` in the project root for a list of available commands.

Install
---

Creates a virtual environment and installs dependencies.

```
$ make install
```

Update
---

Update dependencies.

```
$ make update
```

Shell
---

Activates the virtual environment.

```
$ make shell
```


Test
---

Run tests.

```
$ make test
```


Publish
---

Upload Snow to PyPI.

```
$ make publish
```

Clean
---

Remove cache and bytecode files.

```
$ make clean
```

Lint
---

Check if the code conforms to *Black* and *Flake*, and that type annotations are in place.

```
$ make lint
```


Reformat
---

Reformat library and test code using *black*, *autoflake* and *isort*.

```
$ make reformat
```


