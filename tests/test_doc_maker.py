import unittest
import re
from pyld import jsonld
import requests

from unittest.mock import patch
from hydra_python_core import doc_maker, doc_writer
from samples import doc_writer_sample_output


class TestCreateClass(unittest.TestCase):
    """
        Test Class for create_class method
    """

    def setUp(self):
        self.doc = doc_writer_sample_output.doc

    @patch('hydra_python_core.doc_maker.HydraClass', spec_set=doc_maker.HydraClass)
    def test_output(self, mock_class):
        """
            Test method to check if HydraClass is instantiated with proper arguments and
            properties and operations have been added to it.
        """
        class_dict = {
                "@id": "https://hydrus.com/api/dummyClass",
                "@type": [
                    "http://www.w3.org/ns/hydra/core#Class"
                ],
                "http://www.w3.org/ns/hydra/core#description": [
                    {
                        "@value": "A dummyClass for demo"
                    }
                ],
                "http://www.w3.org/ns/hydra/core#supportedOperation": [
                    {
                        "@type": [
                            "http://schema.org/FindAction"
                        ],
                        "http://www.w3.org/ns/hydra/core#expects": [
                            {
                                "@id": "https://json-ld.org/playground/null"
                            }
                        ],
                        "http://www.w3.org/ns/hydra/core#expectsHeader": [

                        ],
                        "http://www.w3.org/ns/hydra/core#method": [
                            {
                                "@value": "GET"
                            }
                        ],
                        "http://www.w3.org/ns/hydra/core#possibleStatus": [
                            {
                                "@type": [
                                    "http://www.w3.org/ns/hydra/core#Status"
                                ],
                                "http://www.w3.org/ns/hydra/core#description": [
                                    {
                                        "@value": "dummyClass returned."
                                    }
                                ],
                                "http://www.w3.org/ns/hydra/core#statusCode": [
                                    {
                                        "@value": 200
                                    }
                                ],
                                "http://www.w3.org/ns/hydra/core#title": [
                                    {
                                        "@value": ""
                                    }
                                ]
                            }
                        ],
                        "http://www.w3.org/ns/hydra/core#returns": [
                            {
                                "@id": "https://hydrus.com/api/dummyClass"
                            }
                        ],
                        "http://www.w3.org/ns/hydra/core#returnsHeader": [

                        ],
                        "http://www.w3.org/ns/hydra/core#title": [
                            {
                                "@value": "GetClass"
                            }
                        ]
                    }
                ],
                "http://www.w3.org/ns/hydra/core#supportedProperty": [
                    {
                        "@type": [
                            "https://json-ld.org/playground/SupportedProperty"
                        ],
                        "http://www.w3.org/ns/hydra/core#property": [
                            {
                                "@id": "http://props.hydrus.com/prop1"
                            }
                        ],
                        "http://www.w3.org/ns/hydra/core#readable": [
                            {
                                "@value": "false"
                            }
                        ],
                        "http://www.w3.org/ns/hydra/core#required": [
                            {
                                "@value": "false"
                            }
                        ],
                        "http://www.w3.org/ns/hydra/core#title": [
                            {
                                "@value": "Prop1"
                            }
                        ],
                        "http://www.w3.org/ns/hydra/core#writeable": [
                            {
                                "@value": "true"
                            }
                        ]
                    }
                ],
                "http://www.w3.org/ns/hydra/core#title": [
                    {
                        "@value": "dummyClass"
                    }
                ]
            }
        # run the function and check if HydraClass has been instantiated
        class_ = doc_maker.create_class(class_dict, endpoint=False)
        mock_class.assert_called_once_with('dummyClass', 'A dummyClass for demo',
                                           endpoint=False)

        # check if properties and operations has been added to the hydra class
        self.assertEqual(mock_class.return_value.add_supported_op.call_count,
                         len(class_dict["http://www.w3.org/ns/hydra/core#supportedOperation"]))
        self.assertEqual(mock_class.return_value.add_supported_prop.call_count,
                         len(class_dict["http://www.w3.org/ns/hydra/core#supportedProperty"]))
        self.assertIsInstance(class_, doc_writer.HydraClass)


class TestCreateDoc(unittest.TestCase):
    """
        Test Class for create_doc method
    """

    def setUp(self):
        self.doc = doc_writer_sample_output.doc

    @patch('hydra_python_core.doc_maker.re')
    def test_validations(self, mock_re):
        """
            Test method to check if exceptions are raised if doc has missing keys
            or contain syntax errors
        """

        # Check if proper error raised when no "@id" key is present
        id_ = self.doc.pop("@id", None)
        self.assertRaises(SyntaxError, doc_maker.create_doc, self.doc)
        self.doc["@id"] = id_

    @patch('hydra_python_core.doc_maker.HydraDoc', spec_set=doc_maker.HydraDoc)
    def test_output(self, mock_doc):
        """
            Test method to check if HydraDoc are instantiated with proper arguments
            and all necessary functions are called.
        """

        server_url = "http://hydrus.com/"
        api_name = "test_api"
        doc_name = 'vocab'
        class_count = 0
        collection_count = 0
        # find out the number of classes
        for class_ in self.doc["supportedClass"]:
            if 'manages' not in class_:
                class_count += 1
            else:
                collection_count += 1

        # check if apidoc has been created with proper args
        apidoc = doc_maker.create_doc(self.doc, server_url, api_name)
        mock_doc.assert_called_once_with(api_name, "Title for the API Documentation",
                                         "Description for the API Documentation",
                                         api_name, server_url, doc_name)
        # check if all context keys has been added to apidoc
        self.assertEqual(mock_doc.return_value.add_to_context.call_count, len(
            self.doc["@context"].keys()))

        # check if all classes has been added to apidoc
        self.assertEqual(
            mock_doc.return_value.add_supported_class.call_count, class_count-3)
        self.assertEqual(
            mock_doc.return_value.add_supported_collection.call_count, collection_count)

        # check if all base resource and classes has been added
        self.assertEqual(
            mock_doc.return_value.add_baseResource.call_count, 1)
        self.assertEqual(
            mock_doc.return_value.add_baseCollection.call_count, 1)
        self.assertEqual(
            mock_doc.return_value.gen_EntryPoint.call_count, 1)

        self.assertIsInstance(apidoc, doc_writer.HydraDoc)


class TestCreateProperty(unittest.TestCase):
    """
        Test Class for create_property method
    """

    @patch('hydra_python_core.doc_maker.HydraClassProp', spec_set=doc_maker.HydraClassProp)
    def test_output(self, mock_prop):
        """
            Test method to check if HydraClassProp is instantiated with proper agruments with
            different input
        """
        property_ = {
            "@type": [
              "http://www.w3.org/ns/hydra/core#SupportedProperty"
            ],
            "http://www.w3.org/ns/hydra/core#property": [
              {
                "@id": "http://props.hydrus.com/prop1"
              }
            ],
            "http://www.w3.org/ns/hydra/core#readable": [
              {
                "@value": "false"
              }
            ],
            "http://www.w3.org/ns/hydra/core#required": [
              {
                "@value": "false"
              }
            ],
            "http://www.w3.org/ns/hydra/core#title": [
              {
                "@value": "Prop1"
              }
            ],
            "http://www.w3.org/ns/hydra/core#writeable": [
              {
                "@value": "true"
              }
            ]
        }

        doc_maker.create_property(property_)
        mock_prop.assert_called_once_with(prop="http://props.hydrus.com/prop1", title="Prop1",
                                          required="false", read="false", write="true")

        mock_prop.reset_mock()
        property_["http://www.w3.org/ns/hydra/core#readable"] = [
              {
                "@value": "true"
              }
            ]
        doc_maker.create_property(property_)
        mock_prop.assert_called_once_with(prop="http://props.hydrus.com/prop1", title="Prop1",
                                          required="false", read="true", write="true")

        mock_prop.reset_mock()
        property_["http://www.w3.org/ns/hydra/core#property"] = [
              {
                "@id": "http://props.hydrus.com/prop2"
              }
        ]
        obj = doc_maker.create_property(property_)
        mock_prop.assert_called_once_with(prop="http://props.hydrus.com/prop2", title="Prop1",
                                          required="false", read="true", write="true")

        self.assertIsInstance(obj, doc_writer.HydraClassProp)


class TestCreateOperation(unittest.TestCase):
    """
        Test Class for create_operation method
    """

    @patch('hydra_python_core.doc_maker.HydraClassOp', spec_set=doc_maker.HydraClassOp)
    def test_output(self, mock_op):
        """
            Test method to check if HydraClassOp is instantiated with proper arguments with
            different input
        """
        op = {
            "@type": [
              "http://schema.org/UpdateAction"
            ],
            "http://www.w3.org/ns/hydra/core#expects": [
              {
                "@id": "https://hydrus.com/api/dummyClass"
              }
            ],
            "http://www.w3.org/ns/hydra/core#expectsHeader": [

            ],
            "http://www.w3.org/ns/hydra/core#method": [
              {
                "@value": "POST"
              }
            ],
            "http://www.w3.org/ns/hydra/core#possibleStatus": [
            ],
            "http://www.w3.org/ns/hydra/core#returns": [
              {
                "@id": "null"
              }
            ],
            "http://www.w3.org/ns/hydra/core#returnsHeader": [
              {
                "@value": "Content-Type"
              },
              {
                "@value": "Content-Length"
              }
            ],
            "http://www.w3.org/ns/hydra/core#title": [
              {
                "@value": "UpdateClass"
              }
            ]
          }
        doc_maker.create_operation(op)
        mock_op.assert_called_once_with(
            title="UpdateClass",
            method="POST",
            expects="https://hydrus.com/api/dummyClass",
            returns="null",
            returns_header=["Content-Type", "Content-Length"],
            possible_status=[],
            expects_header=[])

        mock_op.reset_mock()
        op["http://www.w3.org/ns/hydra/core#expects"] = [
            {
                "@id": "http://hydrus.com/test"
            }
        ]
        doc_maker.create_operation(op)
        mock_op.assert_called_once_with(
            title="UpdateClass",
            method="POST",
            expects="http://hydrus.com/test",
            returns="null",
            returns_header=["Content-Type", "Content-Length"],
            possible_status=[],
            expects_header=[])

        mock_op.reset_mock()
        op["http://www.w3.org/ns/hydra/core#returns"] = [
            {
                "@id": "http://hydrus.com/test"
            }
        ]
        obj = doc_maker.create_operation(op)
        mock_op.assert_called_once_with(
            title="UpdateClass",
            method="POST",
            expects="http://hydrus.com/test",
            returns="http://hydrus.com/test",
            returns_header=["Content-Type", "Content-Length"],
            possible_status=[],
            expects_header=[])

        self.assertIsInstance(obj, doc_writer.HydraClassOp)


class TestCreateStatus(unittest.TestCase):
    """
        Test Class for create_status method
    """

    @patch('hydra_python_core.doc_maker.HydraStatus', spec_set=doc_maker.HydraStatus)
    def test_output(self, mock_status):
        """
            Test method to check if HydraStatus is instantiated with proper arguments with
            different input
        """

        status = [
              {
                "@type": [
                  "http://www.w3.org/ns/hydra/core#Status"
                ],
                "http://www.w3.org/ns/hydra/core#description": [
                  {
                    "@value": "dummyClass updated."
                  }
                ],
                "http://www.w3.org/ns/hydra/core#statusCode": [
                  {
                    "@value": 200
                  }
                ],
                "http://www.w3.org/ns/hydra/core#title": [
                  {
                    "@value": ""
                  }
                ]
              },
            ]
        obj = doc_maker.create_status(status)
        mock_status.assert_called_once_with(200, None, '', 'dummyClass updated.')
        self.assertIsInstance(obj[0], doc_writer.HydraStatus)


class TestFragments(unittest.TestCase):
    """
        Test Class for checking fragments in id's
    """
    def test_fragments(self):
        server_url = "http://hydrus.com/"
        api_name = "test_api"
        self.doc = doc_writer_sample_output.doc
        apidoc = doc_maker.create_doc(self.doc, server_url, api_name)
        for class_ in apidoc.parsed_classes:
            resource = apidoc.parsed_classes[class_]['class']
            resource_id = resource.id_
            regex = r"(\W*\?resource=\W*)([a-zA-Z]+)"
            match_groups = re.search(regex, resource_id)

            assert match_groups.groups()[0] is not None
            assert match_groups.groups()[1] == class_

        for collection in apidoc.collections:
            resource_id = apidoc.collections[collection]['collection'].collection_id
            regex = r"(\W*\?resource=\W*)([a-zA-Z]+)"
            match_groups = re.search(regex, resource_id)

            assert match_groups.groups()[0] is not None
            assert match_groups.groups()[1] == collection


if __name__ == '__main__':
    unittest.main()
