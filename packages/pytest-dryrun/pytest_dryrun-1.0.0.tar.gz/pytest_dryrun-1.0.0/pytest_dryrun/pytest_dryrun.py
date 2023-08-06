"""
# Pytest Dryrun Plugin

A Pytest plugin to ignore tests during collection without reporting them in the
test summary.
"""
import pytest


def pytest_cmdline_main(config: pytest.Config):
    """
    Make --dryrun and --no-dryrun options mutually exclusive
    """
    if config.getoption('--dryrun') and config.getoption("--no-dryrun"):
        print("The --dryrun and --no-dryrun options are mutually exclusive")
        exit(4)


def pytest_addoption(parser: pytest.Parser):
    """
    Add --dryrun and --no-dryrun options
    """
    parser.addoption(
        "--dryrun",
        action="store_true",
        help="Only run tests that have the dryrun mark",
    )
    parser.addoption(
        "--no-dryrun",
        action="store_true",
        help="Only run tests that don't have the dryrun mark",
    )


def pytest_configure(config: pytest.Config):
    config.addinivalue_line(
        'markers',
        'dryrun: include the given test function in the dryrun test suite',
    )


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """
    Filter out tests to implement --dryrun and --no-dryrun
    behaviour.
    """
    remove_non_dryrun = config.getoption('--dryrun')
    remove_dryrun = config.getoption('--no-dryrun')
    new_items = []
    for item in items:
        if item.get_closest_marker('dryrun') is None:
            if not remove_non_dryrun:
                new_items.append(item)
        else:
            if not remove_dryrun:
                new_items.append(item)

    # Overwrite the old items array
    # https://stackoverflow.com/a/8037476/6335363
    items[:] = new_items
