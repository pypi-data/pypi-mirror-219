# pylint: disable=missing-module-docstring,missing-function-docstring

import pytest


@pytest.mark.parametrize("option", ["-d", "--debug"])
def test_debug_logs(cli_runner, csv_file, option):
    csv = csv_file("sample.csv")
    ret = cli_runner(f"{csv} {option}")
    assert "debug=True" in ret.stdout
