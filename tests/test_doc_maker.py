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


class TestCreateClass(unittest.TestCase):

    def setUp(self):
        self.doc = hydra_doc_sample.doc

    @patch('hydra_python_core.doc_maker.re')
    def test_validations(self, mock_re):
        class_dict = self.doc["supportedClass"][0]
        exclude_list = ['http://www.w3.org/ns/hydra/core#Resource',
                        'http://www.w3.org/ns/hydra/core#Collection',
                        'vocab:EntryPoint']

        entrypoint = doc_maker.get_entrypoint(self.doc)
        class_id = class_dict.pop("@id", None)

        # Check if returning None when class id is a BaseClass or an EntryPoint
        for id_ in exclude_list:
            class_dict["@id"] = id_
            self.assertEqual((None, None, None), doc_maker.create_class(entrypoint, class_dict))

        class_dict["@id"] = class_id

        # Check if returning None when any key is not of proper format
        mock_re.match.return_value = None
        self.assertEqual((None, None, None), doc_maker.create_class(entrypoint, class_dict))

    def test_doc_keys(self):

        doc_keys = {
            "supportedProperty": False,
            "title": False,
            "description": False,
            "supportedOperation": False
        }


class TestClassInEndPoint(unittest.TestCase):

    def setUp(self):
        self.doc = hydra_doc_sample.doc

    def test_validations(self):

        class_dict = self.doc["supportedClass"][0]
        entrypoint = doc_maker.get_entrypoint(self.doc)

        # check if proper exception is raised when supportedProperty key is not present in entrypoint
        properties = entrypoint.pop("supportedProperty")
        self.assertRaises(SyntaxError, doc_maker.class_in_endpoint, class_dict, entrypoint)

        # check if proper exception is raised when property key is not present
        property_ = properties[0].pop("property")
        entrypoint["supportedProperty"] = properties
        self.assertRaises(SyntaxError, doc_maker.class_in_endpoint, class_dict, entrypoint)

        # check if exception is raised when no label key is found in property
        properties[0]["property"] = property_
        label = property_.pop("label")
        self.assertRaises(SyntaxError, doc_maker.collection_in_endpoint, class_dict, entrypoint)
        property_["label"] = label
