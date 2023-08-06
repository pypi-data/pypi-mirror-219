#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from wtforms import Form
from hawthorn.modelutils import ModelBase, get_model_class_name
from hawthorn.restfulwrapper.accesscontrol.authorizedsession import SESSION_UID_KEY
from .definations import Relations, _RESTfulAPIWraper
from .register import register_model_general_api_handlers, register_middle_relation_model_api_handlers, register_model_page_descriptor_api_handler

__all__ = ['restful_api', 'SESSION_UID_KEY']

LOG = logging.getLogger('hawthorn.restfulwrapper')

__restful_api_wrappers: dict[str, _RESTfulAPIWraper] = {}
__page_descriptor_model_wrappers: dict[str, _RESTfulAPIWraper] = {}
__restful_api_registered = False

def restful_api(endpoint: str = '', add_form: Form = None, update_form: Form = None, relations: Relations = None, **kwargs):
    """
    wrapper model as RESTful API endpoint

    usage:  @restful_api(endpoint)
            class ModelName():
                def __init__(self):
                    pass
    """
    def decorator(cls: ModelBase):
        uri = endpoint
        if not uri:
            uri = '/api/' + get_model_class_name(cls).lower() + 's'
            LOG.info('treat %s as RESTful URI:%s', get_model_class_name(cls), uri)
        if uri and uri not in __restful_api_wrappers:
            w = _RESTfulAPIWraper(uri, cls, add_form=add_form, update_form=update_form, relations=relations)
            __restful_api_wrappers[uri] = w
            route_pieces = uri.split('/')
            page_name = route_pieces[len(route_pieces)-1]
            __page_descriptor_model_wrappers[page_name] = w
        else:
            raise ValueError("Duplicate registering model RESTful URI '%s'" % (uri))
        
        return cls
    return decorator

def get_all_restful_api_wrappers():
    return __restful_api_wrappers

def get_page_descriptor_model(pathname: str) -> _RESTfulAPIWraper:
    if pathname in __page_descriptor_model_wrappers:
        return __page_descriptor_model_wrappers[pathname]
    return None

def register_restful_apis():
    global __restful_api_registered
    if not __restful_api_wrappers or __restful_api_registered:
        return
    for endpoint, w in __restful_api_wrappers.items():
        if endpoint and w.cls:
            LOG.info('registing RESTful endpoint %s', endpoint)
            if w.relations:
                register_middle_relation_model_api_handlers(w.cls, endpoint, w.relations.src_field, w.relations.dst_field, w.relations.src_model, w.relations.dst_model)
            else:
                register_model_general_api_handlers(w.cls, endpoint, add_form=w.add_form, edit_form=w.update_form)
    register_model_page_descriptor_api_handler(get_page_descriptor_model)
    __restful_api_registered = True
