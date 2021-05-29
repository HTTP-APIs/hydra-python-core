"""Contsructor to take a Python dict containing an API Documentation and
create a HydraDoc object for it
"""
import re
import json
from pyld import jsonld
import requests
from hydra_python_core.doc_writer import (HydraDoc, HydraClass, HydraClassProp,
                                          HydraClassOp, HydraStatus, HydraLink,
                                          HydraCollection, DocUrl)
from typing import Any, Dict, Match, Optional, Tuple, Union, List
from hydra_python_core.namespace import hydra, rdfs
from urllib.parse import urlparse

jsonld.set_document_loader(jsonld.requests_document_loader())


def create_doc(doc: Dict[str, Any], HYDRUS_SERVER_URL: str = None,
               API_NAME: str = None) -> HydraDoc:
    """
    Create the HydraDoc object from the API Documentation.

    :param doc: dictionary of hydra api doc
    :param HYDRUS_SERVER_URL: url of the hydrus server
    :param API_NAME: name of the api
    :return: instance of HydraDoc which server and agent can understand
    :raise SyntaxError: If the `doc` doesn't have an entry for `@id` , `@context`, `@type` key.
    """

    # These keys must be there in the APIDOC: @context, @id, @type
    if not all(key in doc for key in ('@context', '@id', '@type')):
        raise SyntaxError("Please make sure doc contains @context, @id and @type")

    _context = doc['@context']
    base_url = ''
    entrypoint = ''
    doc_name = 'vocab'
    doc_url = ''
    _id = ''
    _entrypoint = ''
    _title = "The default title"
    _description = "This is the default description"
    _classes = []
    _collections = []
    _endpoints = []
    _possible_status = []
    _endpoint_class = []
    _endpoint_collection = []
    _non_endpoint_classes = []

    expanded_doc = jsonld.expand(doc)
    for item in expanded_doc:
        _id = item['@id']
        # Extract base_url, entrypoint and API name
        base_url = urlparse(_id).scheme + '//' + urlparse(_id).netloc
        entrypoint = _entrypoint
        doc_name = urlparse(_id).path.split('/')[-1]
        doc_url = DocUrl(HYDRUS_SERVER_URL, api_name=API_NAME, doc_name=doc_name).doc_url
        for entrypoint in item[hydra['entrypoint']]:
            _entrypoint = entrypoint['@id']
        if hydra['title'] in item:
            for title in item[hydra['title']]:
                _title = title['@value']
        if hydra['description'] in item:
            for description in item[hydra['description']]:
                _description = description['@value']
        for classes in item[hydra['supportedClass']]:
            isCollection = False
            if hydra['manages'] in classes:
                isCollection = True
                _collections.append(classes)
            for supported_prop in classes[hydra['supportedProperty']]:
                for prop in supported_prop[hydra['property']]:
                    if '@type' in prop:
                        for prop_type in prop['@type']:
                            if prop_type == hydra['Link']:
                                # find the range of the link
                                for resource_range in prop[rdfs['range']]:
                                    _endpoints.append(check_namespace(resource_range['@id']))
            if not isCollection:
                _classes.append(classes)
        for status in item[hydra['possibleStatus']]:
            _possible_status.append(status)
    for classes in _classes:
        if classes['@id'] == hydra['Resource'] or classes['@id'] == hydra['Collection']:
            continue
        endpoint = False
        if classes['@id'].find("EntryPoint") != -1:
            classes['@id'] = "{}{}".format(doc_url, "EntryPoint")
        else:
            classes['@id'] = check_namespace(classes['@id'])
        for endpoints in _endpoints:
            if classes['@id'] == endpoints:
                endpoint = True
                _endpoint_class.append(classes)
        if not endpoint:
            _non_endpoint_classes.append(classes)

    for collections in _collections:
        collections['@id'] = check_namespace(collections['@id'])
        for endpoints in _endpoints:
            if collections['@id'] == endpoints:
                _endpoint_collection.append(collections)
    # Main doc object
    if HYDRUS_SERVER_URL is not None and API_NAME is not None:
        apidoc = HydraDoc(
            API_NAME, _title, _description, API_NAME, HYDRUS_SERVER_URL, doc_name)
    else:
        apidoc = HydraDoc(
            entrypoint, _title, _description, entrypoint, base_url, doc_name)

    # additional context entries
    for entry in _context:
        apidoc.add_to_context(entry, _context[entry])

    # make endpoint classes
    for endpoint_classes in _endpoint_class:
        if endpoint_classes['@id'] == hydra['Resource'] or \
            endpoint_classes['@id'] == hydra['Collection'] or \
                endpoint_classes['@id'].find("EntryPoint") != -1:
            continue
        class_ = create_class(endpoint_classes, endpoint=True)
        apidoc.add_supported_class(class_)

    # make non-endpoint classes
    for classes in _non_endpoint_classes:
        if classes['@id'] == hydra['Resource'] or classes['@id'] == hydra['Collection'] or \
                classes['@id'].find("EntryPoint") != -1:
            continue
        class_ = create_class(classes, endpoint=False)
        apidoc.add_supported_class(class_)

    # make endpoint collections
    for endpoint_collection in _endpoint_collection:
        collection_ = create_collection(endpoint_collection)
        apidoc.add_supported_collection(collection_)

    # add possibleStatus
    status_list = create_status(_possible_status)
    for status in status_list:
        apidoc.add_possible_status(status)

    # add base collection and resource
    apidoc.add_baseResource()
    apidoc.add_baseCollection()
    apidoc.gen_EntryPoint()
    return apidoc


def create_collection(endpoint_collection: Dict[str, Any]) -> HydraCollection:
    """
     Creates the instance of HydraCollection from expanded APIDOC

    :param endpoint_collection: creates HydraCollection from expanded API doc
    :return: instance of HydraCollection

    """
    collection_name = "The default collection name"
    collection_description = "The default collection description"

    if hydra['title'] in endpoint_collection:
        collection_name = endpoint_collection[hydra['title']][0]['@value']

    if hydra['description'] in endpoint_collection:
        collection_description = endpoint_collection[hydra['description']][0]['@value']

    manages = {}
    if hydra['object'] in endpoint_collection[hydra['manages']][0]:
        object_id = endpoint_collection[hydra['manages']][0][hydra['object']][0]['@id']
        manages['object'] = check_namespace(object_id)
    if hydra['subject'] in endpoint_collection[hydra['manages']][0]:
        subject_id = endpoint_collection[hydra['manages']][0][hydra['subject']][0]['@id']
        manages['subject'] = check_namespace(subject_id)
    if hydra['property'] in endpoint_collection[hydra['manages']][0]:
        property_id = endpoint_collection[hydra['manages']][0][hydra['property']][0]['@id']
        manages['property'] = check_namespace(property_id)
    is_get = False
    is_post = False
    is_put = False
    is_del = False

    for supported_operations in endpoint_collection[hydra['supportedOperation']]:
        if supported_operations[hydra['method']][0]['@value'] == 'GET':
            is_get = True
        if supported_operations[hydra['method']][0]['@value'] == 'PUT':
            is_post = True
        if supported_operations[hydra['method']][0]['@value'] == 'POST':
            is_put = True
        if supported_operations[hydra['method']][0]['@value'] == 'PUT':
            is_del = True

    collection_ = HydraCollection(collection_name=collection_name,
                                  collection_description=collection_description,
                                  manages=manages, get=is_get,
                                  post=is_post, put=is_put, delete=is_del)
    return collection_


def create_class(expanded_class: Dict[str, Any], endpoint: bool) -> HydraClass:
    """
    Creates HydraClass from the expanded API document;

    :param apidoc: object of HydraDoc type
    :param expanded_class: the expanded class
    :param endpoint: boolean True if class is an endpoint, False if class is not endpoint
    :return: HydraClass object that can be added to api doc
    """

    class_title = "A Class"
    class_description = "The description of the class"

    if hydra['title'] in expanded_class:
        class_title = expanded_class[hydra['title']][0]['@value']

    if hydra['description'] in expanded_class:
        class_description = expanded_class[hydra['description']][0]['@value']

    class_ = HydraClass(class_title,
                        class_description, endpoint=endpoint)

    # add supported Property
    for supported_property in expanded_class[hydra["supportedProperty"]]:
        prop_ = create_property(supported_property)
        class_.add_supported_prop(prop_)

    # add supported operations
    for supported_operations in expanded_class[hydra['supportedOperation']]:
        op_ = create_operation(supported_operations)
        class_.add_supported_op(op_)

    return class_


def create_operation(supported_operation: Dict[str, Any]) -> HydraClassOp:
    """
    Creates the instance of HydraClassOp

    :param supported_operation: The expanded supported operation from the API DOC
    :return: HydraClassOp
    """
    op_title = "The title of the operation"
    op_expects = "null"
    op_returns = "null"
    op_expects_header = []
    op_returns_header = []
    op_possible_status = []

    if hydra['title'] in supported_operation:
        op_title = supported_operation[hydra['title']][0]['@value']

    op_method = supported_operation[hydra['method']][0]['@value']

    if hydra['expects'] in supported_operation:
        op_expects = check_namespace(supported_operation[hydra['expects']][0]['@id'])

    if hydra['returns'] in supported_operation:
        op_returns = check_namespace(supported_operation[hydra['returns']][0]['@id'])

    if hydra['expectsHeader'] in supported_operation:
        for header in supported_operation[hydra['expectsHeader']]:
            op_expects_header.append(header['@value'])

    if hydra['returnsHeader'] in supported_operation:
        for header in supported_operation[hydra['returnsHeader']]:
            op_returns_header.append(header['@value'])

    if hydra['possibleStatus'] in supported_operation:
        op_possible_status = create_status(supported_operation[hydra['possibleStatus']])

    op_ = HydraClassOp(title=op_title,
                       method=op_method,
                       expects=op_expects,
                       returns=op_returns,
                       expects_header=op_expects_header,
                       returns_header=op_returns_header,
                       possible_status=op_possible_status)
    return op_


def create_status(possible_status: List[Any]) -> List[HydraStatus]:
    """
    Creates instance of HydraStatus from expanded API doc

    :param possible_status: possible status from the expanded API doc
    :return: List of instances of HydraStatus
    """
    status_list = []

    for status in possible_status:
        status_id = None
        status_title = "The default title for status"
        status_desc = "The default description of status"
        if hydra['description'] in status:
            status_desc = status[hydra['description']][0]['@value']
        status_code = status[hydra['statusCode']][0]['@value']

        if '@id' in status:
            status_id = status['@id']

        if hydra['title'] in status:
            status_title = status[hydra['title']][0]['@value']

        status_ = HydraStatus(status_code, status_id, status_title, status_desc)
        status_list.append(status_)

    return status_list


def create_property(supported_property: Dict[str, Any]) -> Union[HydraLink, HydraClassProp]:
    """
    Creates the HydraClassProp from the expanded supported property

    :param supported_property: supported property dict from the expanded api doc
    :return: HydraClassProp
    """
    prop_id = ""
    prop_title = "The title of Property"

    if hydra['property'] in supported_property:
        prop_id = check_namespace(supported_property[hydra['property']][0]['@id'])
        if '@type' in supported_property[hydra['property']][0]:
            if supported_property[hydra['property']][0]['@type'][0] == hydra['Link']:
                prop_id = create_link(supported_property[hydra['property']][0])
    else:
        raise KeyError("{} is missing".format(hydra['property']))

    if hydra['title'] in supported_property:
        prop_title = supported_property[hydra['title']][0]['@value']
    prop_read = supported_property[hydra['readable']][0]['@value']
    prop_require = supported_property[hydra['required']][0]['@value']
    prop_write = supported_property[hydra['writeable']][0]['@value']

    prop_ = HydraClassProp(prop=prop_id,
                           title=prop_title,
                           required=prop_require,
                           read=prop_read,
                           write=prop_write)
    return prop_


def create_link(supported_property: Dict[str, Any]) -> HydraLink:
    """
    Creates the instances of HydraLink

    :param supported_property: expanded Property
    :return: instance of HydraLink
    """
    prop_title = 'The default Link title'
    prop_desc = 'The default Link description'

    prop_id = check_namespace(supported_property['@id'])
    if hydra['description'] in supported_property:
        prop_desc = supported_property[hydra['description']]
    if hydra['title'] in supported_property:
        prop_title = supported_property[hydra['title']][0]['@value']

    prop_domain = check_namespace(supported_property[rdfs['domain']][0]['@id'])
    prop_range = check_namespace(supported_property[rdfs['range']][0]['@id'])

    link_ = HydraLink(prop_id, prop_title, prop_desc, prop_domain, prop_range)

    if hydra['supportedOperation'] in supported_property:
        for operations in supported_property[hydra['supportedOperation']]:
            operation = create_operation(operations)
            link_.add_supported_op(operation)

    return link_


def check_namespace(id_: str = None) -> str:
    """
    A helper method to check if the classes and properties are in the same
    namespace and if not bring them into the right namespace
    :param id_ The id to check
    :return: correct url
    """
    if id_.find(DocUrl.doc_url) == -1 and id_ != "null":
        if id_.find('?resource=') != -1:
            resource_name = id_.split('?resource=')[-1]
            id_ = "{}{}".format(DocUrl.doc_url, resource_name)
        elif id_.find('#type') != -1:
            id_ = "{}{}".format(DocUrl.doc_url, id_.split('#')[-1])
        else:
            return id_
    return id_
