import json

if __name__ == "__main__":
    api_doc = create_doc(sample_document.generate())
    print(json.dumps(api_doc.generate(), indent=4, sort_keys=True))
