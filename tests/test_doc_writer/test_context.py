import unittest
from hydra_python_core.doc_writer import Context
from unittest.mock import MagicMock, patch


class TestContext:

    def test_context_with_nothing(self, get_context):
        """
        Test method to test if correct context is generated when no arguments are passed

        """
        context = get_context
        expected_context = {
            'hydra': 'http://www.w3.org/ns/hydra/core#',
            'property': {
                '@type': '@id',
                '@id': 'hydra:property'
            },
            'supportedClass': 'hydra:supportedClass',
            'supportedProperty': 'hydra:supportedProperty',
            'supportedOperation': 'hydra:supportedOperation',
            'label': 'rdfs:label',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            "xsd": "https://www.w3.org/TR/xmlschema-2/#",
            'domain': {
                '@type': '@id',
                '@id': 'rdfs:domain'
            },
            'ApiDocumentation': 'hydra:ApiDocumentation',
            'range': {
                '@type': '@id',
                '@id': 'rdfs:range'
            },
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'title': 'hydra:title',
            'expects': {
                '@type': '@id',
                '@id': 'hydra:expects'
            },
            'returns': {
                '@id': 'hydra:returns',
                '@type': '@id'
            },
            'entrypoint': {
                '@id': 'hydra:entrypoint',
                '@type': '@id'
            },
            'object': {
                '@id': 'hydra:object',
                '@type': '@id'
            },
            'subject': {
                '@id': 'hydra:subject',
                '@type': '@id'
            },
            'readable': 'hydra:readable',
            'writeable': 'hydra:writeable',
            'possibleStatus': 'hydra:possibleStatus',
            'required': 'hydra:required',
            'method': 'hydra:method',
            'statusCode': 'hydra:statusCode',
            'description': 'hydra:description',
            'expectsHeader': 'hydra:expectsHeader',
            'returnsHeader': 'hydra:returnsHeader',
            'manages': 'hydra:manages',
            'subClassOf': {
                '@id': 'rdfs:subClassOf',
                '@type': '@id'
            },
            'search': 'hydra:search'
        }           
        assert expected_context == context.generate()

    def test_context_with_entrypoint(self, capsys, get_hydra_entrypoint):
        _entrypoint = get_hydra_entrypoint
        context = Context("http://www.hydrus.com/", entrypoint=_entrypoint)
        expected_context = {'EntryPoint': 'http://hydrus.com/test_api/vocab?resource=EntryPoint'}
        assert expected_context == context.generate()

    def test_context_with_class(self, capsys, get_hydra_class):
        _class = get_hydra_class
        context = Context("http://www.hydrus.com/", class_=_class)
        expected_context = {
            'hydra': 'http://www.w3.org/ns/hydra/core#',
            'members': 'http://www.w3.org/ns/hydra/core#member',
            'object': 'http://schema.org/object',
            'dummyClass': 'http://hydrus.com/test_api/vocab?resource=dummyClass'
        }
        assert expected_context == context.generate()

    def test_context_with_collection(self, capsys, get_hydra_collection):
        collection_ = get_hydra_collection
        context = Context("http://www.hydrus.com/", collection=collection_)
        expected_context = {
            'hydra': 'http://www.w3.org/ns/hydra/core#',
            'members': 'http://www.w3.org/ns/hydra/core#member',
            'dummyclasses': 'http://hydrus.com/test_api/vocab?resource=dummyclasses'
        }
        assert expected_context == context.generate()
