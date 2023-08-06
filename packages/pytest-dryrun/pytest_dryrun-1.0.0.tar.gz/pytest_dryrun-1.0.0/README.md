# Pytest Dryrun Plugin

A Pytest plugin to ignore tests during collection without reporting them in the
test summary.

## Installation

With Pip

```sh
$ pip install pytest-dryrun
Successfully installed pytest-dryrun-0.1.0
```

## Usage

When the `--dryrun` flag is passed to Pytest, only tests marked with `dryrun`
will be collected and run.

```py
@pytest.mark.dryrun
def test_thing_one():
    """This test will be run, even during dryruns"""
    box = get_box()
    assert "thing one" in box

def test_thing_two():
    """This test will not by run if the `--dryrun` flag is given to Pytest"""
    box = get_box()
    assert "thing two" in box
```

Tests can also be marked with `dryrun` using the library's export:

```py
from pytest_dryrun import dryrun

@dryrun
def test_thing_one():
    box = get_box()
    assert "thing one" in box
```

If the `--no-dryrun` flag is given, only tests not marked with `dryrun` will be
collected, meaning that in the example above, only `test_thing_two` will be
run.

The `--dryrun` and `--no-dryrun` arguments are mutually-exclusive.
