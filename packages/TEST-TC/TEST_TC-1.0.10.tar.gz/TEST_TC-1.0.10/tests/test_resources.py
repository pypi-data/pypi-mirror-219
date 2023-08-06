import pytest
import logging
from unittest.mock import patch

from tc_uc4.utility.resources import get_configuration, log_exception

### get_configuration ###
@pytest.fixture
def mock_config_file(tmpdir):
    config_file = tmpdir.join("proprerties.toml")
    config_file.write("[section]\nkey = 'value'")
    return 'proprerties.toml'

def test_get_configuration_valid(tmpdir, mock_config_file):
    result = get_configuration("section", config_path=str(tmpdir), config_file=mock_config_file)
    assert isinstance(result, dict)
    assert result["key"] == "value"

def test_get_configuration_invalid_file(tmpdir):
    with pytest.raises(Exception):
        get_configuration("section", config_path=str(tmpdir), config_file="non_existent.toml")

def test_get_configuration_invalid_section(tmpdir, mock_config_file):
    with pytest.raises(Exception):
        get_configuration("non_existent_section", config_path=str(tmpdir), config_file=mock_config_file)

### log_exception ###
def test_log_exception_with_logger(caplog):
    logger = logging.getLogger("test_logger")

    @log_exception(logger)
    def my_function():
        raise Exception("Something went wrong")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(SystemExit):
            my_function()

    assert "There was an exception in my_function" in caplog.text
    assert "Exception: Something went wrong" in caplog.text

def test_log_exception_without_logger(caplog):
    @log_exception()
    def my_function():
        raise Exception("Something went wrong")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(SystemExit):
            my_function()

    assert "" in caplog.text
    assert "" in caplog.text

def test_log_exception_no_exception(caplog):
    logger = logging.getLogger("test_logger")

    @log_exception(logger)
    def my_function():
        return "Success"

    with caplog.at_level(logging.ERROR):
        result = my_function()

    assert result == "Success"
    assert "There was an exception in my_function" not in caplog.text