#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import tornado.web
import tornado.httputil
from wtforms import Form
from hawthorn.asynchttphandler import GeneralTornadoHandler, routes
from hawthorn.modelutils import ModelBase, get_model_class_name
from .accesscontrol.authorizedsession import authorized_session_access_control
from .modelapihandlers import ModelApiHandler
from .relationmodelapihandlers import ModelRelationsApiHandler
from .pagedescriptorhandlers import ModelPageDescriptorsApiHandler

LOG = logging.getLogger('services.generalmodelapi.apihandlers')

def register_model_general_api_handlers(model: ModelBase, uri_prefix: str = '', add_form: Form = None, edit_form: Form = None, web_app: tornado.web.Application=None, **options):
    handler = ModelApiHandler(model=model, add_form=add_form, edit_form=edit_form)
    ac = options.pop('ac', [])
    if not ac:
        ac = [authorized_session_access_control]
    if not uri_prefix:
        uri_prefix = '/' + str(get_model_class_name(model)).lower() + 's'
    if uri_prefix.endswith('/'):
        uri_prefix.rstrip('/')
    if not uri_prefix.startswith('/'):
        uri_prefix = '/' + uri_prefix

    local_routes = []
    local_routes.append((uri_prefix+'/get', GeneralTornadoHandler, dict(callback=handler.handler_get, methods=['GET'], ac=ac)))
    local_routes.append((uri_prefix+'/list', GeneralTornadoHandler, dict(callback=handler.handler_list, methods=['GET'], ac=ac)))
    local_routes.append((uri_prefix+'/add', GeneralTornadoHandler, dict(callback=handler.handler_add, methods=['POST'], ac=ac)))
    local_routes.append((uri_prefix+'/edit', GeneralTornadoHandler, dict(callback=handler.handler_edit, methods=['PATCH'], ac=ac)))
    local_routes.append((uri_prefix+'/delete', GeneralTornadoHandler, dict(callback=handler.handler_delete, methods=['DELETE'], ac=ac)))

    if web_app:
        [web_app.add_handlers(route[0], route) for route in local_routes]
    else:
        routes.routes.extend(local_routes)

def register_middle_relation_model_api_handlers(model: ModelBase, uri_prefix: str, src_field: str, dst_field: str, src_model: ModelBase, dst_model: ModelBase, web_app: tornado.web.Application=None, **options):
    handler = ModelRelationsApiHandler(model, src_field, dst_field, src_model, dst_model)
    ac = options.pop('ac', [])
    if not ac:
        ac = [authorized_session_access_control]
    if not uri_prefix:
        uri_prefix = '/' + str(get_model_class_name(model)).lower() + 's'
    if uri_prefix.endswith('/'):
        uri_prefix.rstrip('/')
    if not uri_prefix.startswith('/'):
        uri_prefix = '/' + uri_prefix

    local_routes = []
    local_routes.append((uri_prefix+'/list', GeneralTornadoHandler, dict(callback=handler.handler_relation_ids, methods=['GET'], ac=ac)))
    local_routes.append((uri_prefix+'/add', GeneralTornadoHandler, dict(callback=handler.handler_add, methods=['POST'], ac=ac)))
    local_routes.append((uri_prefix+'/update', GeneralTornadoHandler, dict(callback=handler.handler_update, methods=['PATCH'], ac=ac)))
    local_routes.append((uri_prefix+'/delete', GeneralTornadoHandler, dict(callback=handler.handler_delete, methods=['DELETE'], ac=ac)))

    if web_app:
        [web_app.add_handlers(route[0], route) for route in local_routes]
    else:
        routes.routes.extend(local_routes)

def register_model_page_descriptor_api_handler(get_page_descriptor_model, web_app: tornado.web.Application=None, **options):
    handler = ModelPageDescriptorsApiHandler(get_page_descriptor_model)
    ac = options.pop('ac', [])
    if not ac:
        ac = [authorized_session_access_control]
    local_routes = [
        ('/api/pages/descriptors', GeneralTornadoHandler, dict(callback=handler.handler_get, methods=['GET'], ac=ac))
    ]
    if web_app:
        [web_app.add_handlers(route[0], route) for route in local_routes]
    else:
        routes.routes.extend(local_routes)
