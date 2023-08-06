import pytest
import arrow

from click.testing import CliRunner
from cli import (
    main,
    check_time,
    make_time,
    echo_time,
    echo_error
)


def test_check_time():
    true_times = ["now", "1400"]
    false_times = ["2700", "1461", "00000", "000"]

    for time in true_times:
        assert check_time(time)
    for time in false_times:
        assert not check_time(time)


def test_make_time():
    time_now = "now"
    time_1400 = "1400"

    assert type(make_time(time_now)) == arrow.arrow.Arrow
    assert type(make_time(time_1400)) == arrow.arrow.Arrow


def test_echo_time():
    time = arrow.now()

    assert type(echo_time(time)) == str


def test_echo_error():
    time = arrow.now()

    assert type(echo_error(time)) == str


def test_main():
    runner = CliRunner()
    time_args = ["now", "1400", "140", "2700", "0067", "xxxx"]
    for time in time_args:
        result = runner.invoke(main, [time])
        assert result.exit_code == 0
        assert type(result.output) == str

    # default arguement "now"
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert type(result.output) == str
