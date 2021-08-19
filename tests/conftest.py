import pytest
from hydra_python_core.doc_writer import HydraClass
from hydra_python_core.doc_writer import HydraEntryPoint
from hydra_python_core.doc_writer import HydraCollection
from hydra_python_core.doc_writer import Context
from samples import doc_writer_sample_output

@pytest.fixture(name="get_hydra_class")
def get_hydra_class():
    # Creating classes for the API
    class_title = "dummyClass"                      # Title of the Class
    class_description = "A dummyClass for demo"     # Description of the class
    class_ = HydraClass(class_title, class_description, endpoint=False)
    return class_

@pytest.fixture(name="get_hydra_entrypoint")
def get_hydraentrypoint():
    #Creating HydraEntrypoint
    base_url = "http://www.hydrus.com/"
    entrypoint = "test_api"
    hydra_entrypoint = HydraEntryPoint(base_url,entrypoint)
    return hydra_entrypoint

@pytest.fixture(name="get_hydra_collection")
def get_hydra_collection(get_hydra_class):
    #Creating HydraEntrypoint
    class_ = get_hydra_class
    collection_title = "dummyClass collection"
    collection_name = "dummyclasses"
    collection_description = "This collection comprises of instances of dummyClass"
    collection_managed_by = {
        "property": "rdf:type",
        "object": class_.id_,
    }

    collection_ = HydraCollection(collection_name=collection_name,
                                collection_description=collection_description, manages=collection_managed_by, get=True,
                                post=True, collection_path="DcTest")
    return collection_

@pytest.fixture(name="get_context")
def get_context():
    context = Context('https://hydrus.com/')
    return context

@pytest.fixture(name="get_doc")
def get_doc():
    doc = doc_writer_sample_output.doc
    return doc