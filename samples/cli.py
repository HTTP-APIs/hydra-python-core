import json
from hydra_python_core.doc_maker import  create_doc
from samples.doc_writer_sample_output import doc
if __name__ == "__main__":
    api_doc = create_doc(doc)
    print(json.dumps(api_doc.generate(), indent=4, sort_keys=True))
