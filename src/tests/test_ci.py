## Test dataset information
import logging
import unittest

from src.data import Dataset
from src import workflow
from src.log import logger


class TestDatasetsSmall(unittest.TestCase):
    """
    Basic smoke tests to ensure that the smaller (and more quickly processed)
    available datasets load and have some expected property.
    """
    def test_20_newsgroups(self):
        ds = Dataset.load('20_newsgroups')
        ds = Dataset.load('20_newsgroups')
        assert len(ds.data) == 18846
        assert len(ds.target) == 18846
        assert len(ds.TARGET_NAMES) == 20

    def test_20_newsgroups_pruned(self):
        ds = Dataset.load('20_newsgroups_pruned')
        ds = Dataset.load('20_newsgroups_pruned')
        assert len(ds.TARGET_NAMES) == 20
        assert len(ds.COLOR_KEY) == 21

def test_logging_is_debug_level():
    assert logger.getEffectiveLevel() == logging.DEBUG
