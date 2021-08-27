class TestHydraCollection:

    def test_hydracollection(self, capsys, get_hydra_collection):
        hydra_collection = get_hydra_collection
        expected = {
            '@id': 'http://hydrus.com/test_api/vocab?resource=dummyclasses',
            '@type': 'Collection',
            'subClassOf': 'http://www.w3.org/ns/hydra/core#Collection',
            'title': 'dummyclasses',
            'description': 'This collection comprises of instances of dummyClass',
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
            'supportedProperty': [
                {
                '@type': 'SupportedProperty',
                'title': 'members',
                'required': False,
                'readable': True,
                'writeable': True,
                'property': 'http://www.w3.org/ns/hydra/core#member',
                'description': 'The members of dummyclasses'
                }
            ],
            'manages': {
                'property': 'rdf:type',
                'object': 'http://hydrus.com/test_api/vocab?resource=dummyClass'
            }
        }
        assert expected == hydra_collection.generate()