from hydra_python_core.doc_writer import HydraClassProp
from hydra_python_core.doc_writer import HydraClassOp
from hydra_python_core.doc_writer import HydraStatus

class TestHydraClass:
    
    def test_hydraclass(self,get_hydra_class):
        class_ = get_hydra_class
        expected = {
            '@id': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
            '@type': 'hydra:Class',
            'title': 'dummyClass',
            'description': 'A dummyClass for demo',
            'supportedProperty': [],
            'supportedOperation': []
        }
        assert expected == class_.generate()
    
    def test_hydraclass_op(self, get_hydra_class):
        class2_ = get_hydra_class
        op_status = [HydraStatus(code=200, desc="dummyClass deleted.")]
        op = HydraClassOp("DeleteClass", "DELETE", class2_.id_, None, [], [], op_status)

        class2_.add_supported_op(op)
        expected_context = {
            '@id': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
            '@type': 'hydra:Class',
            'title': 'dummyClass',
            'description': 'A dummyClass for demo',
            'supportedProperty': [],
            'supportedOperation': [
                {
                '@type': 'http://schema.org/DeleteAction',
                'title': 'DeleteClass',
                'method': 'DELETE',
                'expects': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
                'returns': None,
                'expectsHeader': [],
                'returnsHeader': [],
                'possibleStatus': [
                    {
                    '@context': 'https://www.w3.org/ns/hydra/core',
                    '@type': 'Status',
                    'statusCode': 200,
                    'title': '',
                    'description': 'dummyClass deleted.'
                    }
                ]
                }
            ]
        }
        assert expected_context == class2_.generate()


    def test_hydraclass_prop(self, get_hydra_class):
        class_ = get_hydra_class
        prop1_uri = "http://props.hydrus.com/prop1"
        prop1_title = "Prop1"                   
        # Title of the property
        dummyProp1 = HydraClassProp(prop1_uri, prop1_title,
                                    required=False, read=False, write=True)

        class_.add_supported_prop(dummyProp1)
        
        expected_context = {
            '@id': 'http://hydrus.com/test_api/vocab?resource=dummyClass',
            '@type': 'hydra:Class',
            'title': 'dummyClass',
            'description': 'A dummyClass for demo',
            'supportedProperty': [
                {
                '@type': 'SupportedProperty',
                'title': 'Prop1',
                'required': False,
                'readable': False,
                'writeable': True,
                'property': 'http://props.hydrus.com/prop1'
                }
            ],
            'supportedOperation': []
        }
        assert expected_context == class_.generate()