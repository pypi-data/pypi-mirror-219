from typer.testing import CliRunner
from pgperf.pgperf import app
from pgperf.__version__ import __version__


runner = CliRunner()


def test_pgperf_server_configuration_replication_help():
    result = runner.invoke(
        app, ["--conf", "test", "server", "configuration", "replication", "--help"])
    assert result.exit_code == 0


def test_pgperf_server_configuration_replication_sending():
    result = runner.invoke(
        app, ["--conf", "test", "server", "configuration", "replication", "sending"])
    assert result.exit_code == 0


def test_pgperf_server_configuration_replication_primary():
    result = runner.invoke(
        app, ["--conf", "test", "server", "configuration", "replication", "primary"])
    assert result.exit_code == 0


def test_pgperf_server_configuration_replication_standby():
    result = runner.invoke(
        app, ["--conf", "test", "server", "configuration", "replication", "standby"])
    assert result.exit_code == 0


def test_pgperf_server_configuration_replication_subscribers():
    result = runner.invoke(
        app, ["--conf", "test", "server", "configuration", "replication", "subscribers"])
    assert result.exit_code == 0
