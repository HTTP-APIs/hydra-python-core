import yaml
from doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp

with open("openapi_sample.yaml", 'r') as stream:
    try:
        doc = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
info=doc["info"]
desc = info["description"]
title = info["title"]
baseURL = doc["host"]
name = doc["basePath"]
api_doc = HydraDoc(name,title,desc,name,baseURL)
"""get title , desc, props ,ops"""
definitions = doc["definitions"]
paths = doc["paths"]
definitionSet = set()
classAndClassDefinition=dict()
for class_ in definitions:
    try:
        desc = definitions[class_]["description"]
    except KeyError:
        desc = class_
    classDefinition = HydraClass(class_, class_, desc, endpoint=False)
    properties = definitions[class_]["properties"]
    for prop in properties:
        new_prop = HydraClassProp("vocab:" + prop, prop, required=False, read=True, write=True)
        classDefinition.add_supported_prop(new_prop)
    api_doc.add_supported_class(classDefinition, collection=False)

    definitionSet.add(class_)
    classAndClassDefinition[class_]=classDefinition
    # enter class _ with classDefinition in the hashmap so that we can use that later when we add to apidoc
    # maybe we should add here , then if path found we will reference it again and pass to apidoc again
for path in paths:
    possiblePath=path.split('/')[1]
    #dirty hack , do case insensitive search more gracefully
    possiblePath=possiblePath.replace(possiblePath[0], possiblePath[0].upper())
    # check if the path name exists in the classes defined
    if possiblePath in definitionSet:
        for method in paths[path]:
            op_name = ""
            op_method = method
            op_expects = ""
            op_returns = None
            op_status = [{"statusCode": 200, "description": "dummyClass updated"}]
            try:
                op_name = paths[path][method]["summary"]
            except KeyError:
                op_name = possiblePath
            try:
                parameters = paths[path][method]["parameters"]
                for param in parameters:
                    op_expects=param["schema"]["$ref"].split('/')[2]
            except KeyError:
                op_expects=None
            classAndClassDefinition[possiblePath].add_supported_op(HydraClassOp(op_name,op_method,op_expects,op_returns,op_status))
            api_doc.add_supported_class(classAndClassDefinition[possiblePath], collection=False)

    else :
        print("not hit")


# iterate over hash map or definition set to add this g









api_doc.add_baseCollection()
api_doc.add_baseResource()
api_doc.gen_EntryPoint()
hydra_doc = api_doc.generate()
if __name__ == "__main__":
    import json
    dump = json.dumps(hydra_doc, indent=4, sort_keys=True)
    hydra_doc = '''"""\nGenerated API Documentation for Server API using server_doc_gen.py."""\n\ndoc = %s''' % dump
    hydra_doc = hydra_doc + '\n'
    hydra_doc = hydra_doc.replace('true', '"true"')
    hydra_doc = hydra_doc.replace('false', '"false"')
    hydra_doc = hydra_doc.replace('null', '"null"')
    f = open("hydra_doc_sample.py", "w")
    f.write(hydra_doc)
    f.close()

