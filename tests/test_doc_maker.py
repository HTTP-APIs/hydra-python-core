import unittest
import re

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

    def test_output(self):
        entrypoint = doc_maker.get_entrypoint(self.doc)
        class_dict = {
            "@id": "vocab:Pet",
            "@type": "hydra:Class",
            "title": "Pet",
            "description": "Pet",
            "supportedProperty": [],
            "supportedOperation": [],
        }

        expected_output = (False, None)
        self.assertEqual(doc_maker.class_in_endpoint(class_dict, entrypoint), expected_output)

        # Only the title of the class is needed in the method
        class_dict["title"] = "Order"
        expected_output = (True, '/store/order')
        self.assertEqual(doc_maker.class_in_endpoint(class_dict, entrypoint), expected_output)


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

    def test_output(self):
        entrypoint = doc_maker.get_entrypoint(self.doc)
        class_dict = {
            "@id": "vocab:Pet",
            "@type": "hydra:Class",
            "title": "Pet",
            "description": "Pet",
            "supportedProperty": [],
            "supportedOperation": [],
        }

        expected_output = (True, '/pet')
        self.assertEqual(doc_maker.collection_in_endpoint(class_dict, entrypoint), expected_output)

        # Only the title of the class is needed in the method
        class_dict["title"] = "Order"
        expected_output = (False, None)
        self.assertEqual(doc_maker.collection_in_endpoint(class_dict, entrypoint), expected_output)


class TestCreateDoc(unittest.TestCase):

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

    @patch('hydra_python_core.doc_maker.HydraDoc', spec_set=doc_maker.HydraDoc)
    def test_output(self, mock_doc):
        server_url = "test_url"
        api_name = "test_api"

        class_count = 0

        # find out the number of classes
        for class_ in self.doc["supportedClass"]:
            collection = re.match(r'(.*)Collection(.*)', class_["title"], re.M | re.I)
            if not collection:
                class_count += 1

        # check if apidoc has been created with proper args
        doc_maker.create_doc(self.doc, server_url, api_name)
        mock_doc.assert_called_once_with(api_name, self.doc["title"], self.doc["description"],
                                         api_name, server_url)

        # check if all context keys has been added to apidoc
        self.assertEqual(mock_doc.return_value.add_to_context.call_count, len(self.doc["@context"].keys()))

        # check if all classes has been added to apidoc
        self.assertEqual(mock_doc.return_value.add_supported_class.call_count, class_count - 2)

        # check if all base resource and classes has been added
        mock_doc.return_value.add_baseResource.assert_called_once()
        mock_doc.return_value.add_baseCollection.assert_called_once()
        mock_doc.return_value.gen_EntryPoint.assert_called_once()


class TestCreateProperty(unittest.TestCase):

    @patch('hydra_python_core.doc_maker.HydraClassProp', spec_set=doc_maker.HydraClassProp)
    def test_output(self, mock_prop):
        property_ = {
            "@type": "SupportedProperty",
            "property": "",
            "readonly": "true",
            "required": "false",
            "title": "code",
            "writeonly": "true"
        }

        doc_maker.create_property(property_)
        mock_prop.assert_called_once_with(property_["property"], property_["title"],
                                          required=False, read=True, write=True)

        mock_prop.reset_mock()
        property_["readonly"] = "false"
        doc_maker.create_property(property_)
        mock_prop.assert_called_once_with(property_["property"], property_["title"],
                                          required=False, read=False, write=True)

        mock_prop.reset_mock()
        property_["property"] = "test"
        doc_maker.create_property(property_)
        mock_prop.assert_called_once_with(property_["property"], property_["title"],
                                          required=False, read=False, write=True)


class TestCreateOperation(unittest.TestCase):

    @patch('hydra_python_core.doc_maker.HydraClassOp', spec_set=doc_maker.HydraClassOp)
    def test_output(self, mock_op):
        op = {
            "@type": "http://schema.org/UpdateAction",
            "expects": "null",
            "method": "POST",
            "possibleStatus": [
                {
                    "description": "successful operation",
                    "statusCode": 200
                }
            ],
            "returns": "null",
            "title": "uploads an image"
        }
        doc_maker.create_operation(op)
        mock_op.assert_called_once_with(op["title"], op["method"], None, None, op["possibleStatus"])

        mock_op.reset_mock()
        op["expects"] = "test"
        doc_maker.create_operation(op)
        mock_op.assert_called_once_with(op["title"], op["method"], "test", None, op["possibleStatus"])

        mock_op.reset_mock()
        op["returns"] = "test"
        doc_maker.create_operation(op)
        mock_op.assert_called_once_with(op["title"], op["method"], "test", "test", op["possibleStatus"])


class TestCreateStatus(unittest.TestCase):

    @patch('hydra_python_core.doc_maker.HydraStatus', spec_set=doc_maker.HydraStatus)
    def test_output(self, mock_status):
        status = {
            "title": "test",
            "description": "null",
            "statusCode": 405
        }

        obj = doc_maker.create_status(status)
        mock_status.assert_called_once_with(status["statusCode"], status["title"], None)

        self.assertIsInstance(obj, doc_writer.HydraStatus)
