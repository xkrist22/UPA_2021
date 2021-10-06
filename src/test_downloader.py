import json
from requests.models import DecodeError
from downloader import Downloader
import pytest
import os

@pytest.fixture
def json_dataset():
    return "http://www.stud.fit.vutbr.cz/~xkrist22/files/UPA_TEST.json"
@pytest.fixture
def csv_dataset():
    return "http://www.stud.fit.vutbr.cz/~xkrist22/files/UPA_TEST.csv"
@pytest.fixture
def parsed_dataset():
    return [
	    ["a", "b", "c"],
	    ["1", "2", "3"]
    ]
@pytest.fixture
def test_file():
    return "testfile.test"


def test_json(json_dataset, parsed_dataset, test_file):
    dataset = Downloader.get_data(json_dataset, "json")
    assert dataset == parsed_dataset

    dataset = Downloader.get_data(json_dataset, "json", test_file)
    assert os.path.exists(test_file)

    # teardown
    os.remove(test_file)


def test_csv(csv_dataset, parsed_dataset, test_file):
    dataset = Downloader.get_data(csv_dataset, "csv")
    assert dataset == parsed_dataset

    dataset = Downloader.get_data(csv_dataset, "csv", test_file)
    assert os.path.exists(test_file)

    # teardown
    os.remove(test_file)


def test_exception(json_dataset):
    with pytest.raises(AttributeError):
        Downloader.get_data(json_dataset, "unsupported")
