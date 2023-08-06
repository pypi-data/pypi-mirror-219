from pathlib import Path
from config import config
from powerbot_backtesting.models.exporter_models import BaseExporter


def test_base_exporter_cache_path_if_string_is_provided_without_pb_cache():
    """
    This test evaluates whether the correct path is returned if cache_path is provided as a string, but without the substring "__cache_path__".
    """
    exporter = BaseExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'], cache_path="data")

    assert exporter.cache_path == Path("data/__pb_cache__")


def test_base_exporter_cache_path_if_string_is_provided_with_pb_cache():
    """
    This test evaluates whether the correct path is returned if cache_path is provided as a string, including the substring "__cache_path__".
    """

    exporter = BaseExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'], cache_path="data/__pb_cache__")

    assert exporter.cache_path == Path("data/__pb_cache__")


def test_base_exporter_cache_path_if_Path_is_provided_without_pb_cache():
    """
    This test evaluates whether the correct path is returned if cache_path is provided as a Path, but without the substring "__cache_path__".
    """

    exporter = BaseExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'], cache_path=Path("data"))

    assert exporter.cache_path == Path("data/__pb_cache__")


def test_base_exporter_cache_path_if_Path_is_provided_with_pb_cache():
    """
    This test evaluates whether the correct path is returned if cache_path is provided as a Path, including the substring "__cache_path__".
    """

    exporter = BaseExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'], cache_path=Path("data/__pb_cache__"))

    assert exporter.cache_path == Path("data/__pb_cache__")


def test_base_exporter_cache_path_if_no_cache_path_is_provided():
    """
    This test evaluates whether the correct path is returned if cache_path is not provided.
    """

    exporter = BaseExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'])

    assert exporter.cache_path == Path("__pb_cache__")


def test_base_exporter_cache_path_if_empty_Path_object_is_provided():
    """
    This test evaluates whether the correct path is returned if cache_path is not provided.
    """

    exporter = BaseExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'], cache_path=Path())

    assert exporter.cache_path == Path("__pb_cache__")
