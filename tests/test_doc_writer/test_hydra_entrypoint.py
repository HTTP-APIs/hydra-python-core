from _pytest.capture import capsys
from hydra_python_core.doc_writer import HydraEntryPoint

class TestEntryPoint:

    def test_hydraentrypoint(self, capsys, get_hydra_entrypoint):
        _hydra_entrypoint = get_hydra_entrypoint
        expected = {
            '@id': 'http://www.hydrus.com/test_api#EntryPoint',
            '@type': 'hydra:Class',
            'title': 'EntryPoint',
            'description': 'The main entry point or homepage of the API.',
            'supportedProperty': [],
            'supportedOperation': [
                {
                '@id': '_:entry_point',
                '@type': 'http://www.hydrus.com//test_api#EntryPoint',
                'method': 'GET',
                'description': 'The APIs main entry point.',
                'expects': None,
                'returns': None,
                'expectsHeader': [],
                'returnsHeader': [],
                'possibleStatus': []
                }
            ]
        }
        assert expected == _hydra_entrypoint.generate()

    def test_hydraentrypoint_get(self,get_hydra_entrypoint):
        _hydra_entrypoint = get_hydra_entrypoint
        expected = {
        '@context': 'http://www.hydrus.com/test_api/contexts/EntryPoint.jsonld',
        '@id': 'http://www.hydrus.com/test_api',
        '@type': 'EntryPoint'
        }
        assert expected == _hydra_entrypoint.get()

    def test_hydraentrypoint_add_class(self,get_hydra_class,get_hydra_entrypoint):
        _hydra_entrypoint = get_hydra_entrypoint
        _hydra_entrypoint.add_Class(get_hydra_class)
        expected = {
        '@context': 'http://www.hydrus.com/test_api/contexts/EntryPoint.jsonld',
        '@id': 'http://www.hydrus.com/test_api',
        '@type': 'EntryPoint',
        'dummyClass': 'http://www.hydrus.com/test_api/dummyClass'
        }
        assert expected == _hydra_entrypoint.get()

    def test_hydraentrypoint_add_collection(self,capsys, get_hydra_collection,get_hydra_entrypoint):
        _hydra_entrypoint = get_hydra_entrypoint
        _hydra_collection = get_hydra_collection
        _hydra_entrypoint.add_Collection(_hydra_collection)
        expected = {
            '@context': 'http://www.hydrus.com/test_api/contexts/EntryPoint.jsonld',
            '@id': 'http://www.hydrus.com/test_api',
            '@type': 'EntryPoint',
            'collections': [
                {
                '@id': 'http://www.hydrus.com/test_api/DcTest',
                'title': 'dummyclasses',
                '@type': 'Collection',
                'supportedOperation': [
                    {
                    '@id': '_:dummyclasses_retrieve',
                    '@type': 'http://schema.org/FindAction',
                    'method': 'GET',
                    'description': 'Retrieves all the members of dummyclasses',
                    'expects': None,
                    'returns': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
                    'expectsHeader': [
                        
                    ],
                    'returnsHeader': [
                        
                    ],
                    'possibleStatus': [
                        
                    ]
                    },
                    {
                    '@id': '_:dummyclasses_create',
                    '@type': 'http://schema.org/AddAction',
                    'method': 'PUT',
                    'description': 'Create new member in dummyclasses',
                    'expects': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
                    'returns': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
                    'expectsHeader': [
                        
                    ],
                    'returnsHeader': [
                        
                    ],
                    'possibleStatus': [
                        {
                        '@context': 'https://www.w3.org/ns/hydra/core',
                        '@type': 'Status',
                        'statusCode': 201,
                        'title': '',
                        'description': 'A new member in dummyclasses created'
                        }
                    ]
                    },
                    {
                    '@id': '_:dummyclasses_update',
                    '@type': 'http://schema.org/UpdateAction',
                    'method': 'POST',
                    'description': 'Update member of  dummyclasses ',
                    'expects': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
                    'returns': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
                    'expectsHeader': [
                        
                    ],
                    'returnsHeader': [
                        
                    ],
                    'possibleStatus': [
                        {
                        '@context': 'https://www.w3.org/ns/hydra/core',
                        '@type': 'Status',
                        'statusCode': 200,
                        'title': '',
                        'description': 'If the entity was updatedfrom dummyclasses.'
                        }
                    ]
                    },
                    {
                    '@id': '_:dummyclasses_delete',
                    '@type': 'http://schema.org/DeleteAction',
                    'method': 'DELETE',
                    'description': 'Delete member of dummyclasses ',
                    'expects': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
                    'returns': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
                    'expectsHeader': [
                        
                    ],
                    'returnsHeader': [
                        
                    ],
                    'possibleStatus': [
                        {
                        '@context': 'https://www.w3.org/ns/hydra/core',
                        '@type': 'Status',
                        'statusCode': 200,
                        'title': '',
                        'description': 'If entity was deletedsuccessfully from dummyclasses.'
                        }
                    ]
                    }
                ],
                'manages': {
                    'property': 'rdf:type',
                    'object': 'http://hydrus.com/test_api/vocab?resource=dummyClass'
                }
                }
            ]
        }
        assert expected == _hydra_entrypoint.get()
        
