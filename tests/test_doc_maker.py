import unittest

from unittest.mock import patch
from unittest.mock import MagicMock
from hydra_python_core import doc_maker, doc_writer
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

    @patch('hydra_python_core.doc_maker.HydraClass', spec_set=doc_maker.HydraClass)
    def test_output(self, mock_class):

        entrypoint = doc_maker.get_entrypoint(self.doc)
        class_dict = {
            "@id": "vocab:Pet",
            "@type": "hydra:Class",
            "title": "Pet",
            "description": "Pet",
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "",
                    "readonly": "true",
                    "required": "false",
                    "title": "id",
                    "writeonly": "true"
                }
            ],
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Pet",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Invalid input",
                            "statusCode": 405
                        }
                    ],
                    "returns": "null",
                    "title": "Add a new pet to the store"
                }
            ],
        }
        expected_collection = True
        expected_path = '/pet'

        # run the function and check if HydraClass has been instantiated
        class_, collection, collection_path = doc_maker.create_class(entrypoint, class_dict)
        mock_class.assert_called_once_with('Pet', 'Pet', 'Pet', None, False)

        # check if properties and operations has been added to the hydra class
        self.assertEqual(mock_class.return_value.add_supported_op.call_count, 1)
        self.assertEqual(mock_class.return_value.add_supported_prop.call_count, 1)

        self.assertEqual(collection, expected_collection)
        self.assertEqual(collection_path, expected_path)


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


class TestCollectionInEndpoint(unittest.TestCase):

    def setUp(self):
        self.doc = hydra_doc_sample.doc

    def test_validations(self):
        class_dict = self.doc["supportedClass"][0]
        entrypoint = doc_maker.get_entrypoint(self.doc)

        # check if proper exception is raised when supportedProperty key is not present in entrypoint
        properties = entrypoint.pop("supportedProperty")
        self.assertRaises(SyntaxError, doc_maker.collection_in_endpoint, class_dict, entrypoint)

        # check if proper exception is raised when property key is not present
        property_ = properties[0].pop("property")
        entrypoint["supportedProperty"] = properties
        self.assertRaises(SyntaxError, doc_maker.collection_in_endpoint, class_dict, entrypoint)

        # check if exception is raised when no label key is found in property
        properties[0]["property"] = property_
        label = property_.pop("label")
        self.assertRaises(SyntaxError, doc_maker.collection_in_endpoint, class_dict, entrypoint)
        property_["label"] = label


class TestCreateDoc(unittest.TestCase):

    #TODO: check if server url and api name is passed as parameter

    def setUp(self):
        self.doc = hydra_doc_sample.doc

    @patch('hydra_python_core.doc_maker.re')
    def test_validations(self, mock_re):

        # Check if proper error raised when no "@id" key is present
        id_ = self.doc.pop("@id", None)
        self.assertRaises(SyntaxError, doc_maker.create_doc, self.doc)
        self.doc["@id"] = id_

        # Check if proper exception is raised if any key is not of proper format
        mock_re.match.return_value = None
        self.assertRaises(SyntaxError, doc_maker.create_doc, self.doc)
