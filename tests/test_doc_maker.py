import unittest

from unittest.mock import patch
from unittest.mock import MagicMock
from hydra_python_core import doc_maker
from samples import hydra_doc_sample


class TestGetEntrypoint(unittest.TestCase):

    def setUp(self):
        self.doc = hydra_doc_sample.doc

    @patch('hydra_python_core.doc_maker.re')
    def test_validations(self, mock_re):

        # check if proper exception is raised when no "@id" key is present in any supported class
        id_ = self.doc["supportedClass"][0].pop("@id")
        self.assertRaises(SyntaxError, doc_maker.get_entrypoint, self.doc)

        self.doc["supportedClass"][0]["@id"] = id_

        # check if proper exception is raised when no entrypoint match is found
        mock_re.match.return_value = None
        self.assertRaises(SyntaxError, doc_maker.get_entrypoint, self.doc)

