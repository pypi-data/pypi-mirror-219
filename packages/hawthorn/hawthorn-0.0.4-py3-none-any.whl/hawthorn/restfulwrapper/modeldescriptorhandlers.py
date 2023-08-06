#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import tornado.web
import tornado.httputil
import sqlalchemy
import i18n
from http import HTTPStatus
from typing import Iterable
from wtforms import Form
from hawthorn.asynchttphandler import GeneralTornadoHandler, request_body_as_json
from hawthorn.modelutils import ModelBase, model_columns, get_model_class_name
from hawthorn.dbproxy import DbProxy
from hawthorn.valueobjects.resultcodes import RESULT_CODE
from hawthorn.valueobjects.responseobject import GeneralResponseObject, ListResponseObject

from .utils import format_model_query_conditions, read_request_parameters, get_locale_params

LOG = logging.getLogger('services.generalmodelapi.apihandlers')

class ModelPageDescriptorsApiHandler():
    """
    Model page descriptor API handler wrapper
    """
    def __init__(self, model: ModelBase, add_form: Form, edit_form: Form):
        self.model = model
        self.add_form = add_form
        self.edit_form = edit_form

    async def handler_get(self, handler: GeneralTornadoHandler, request: tornado.httputil.HTTPServerRequest):
        """
        API handler of get single model data
        """
        filters = read_request_parameters(request)
        locale_params = get_locale_params(request)
        
        result = GeneralResponseObject(RESULT_CODE.DATA_DOES_NOT_EXISTS, message=i18n.t('basic.data_not_exists', **locale_params))
        while result.code != RESULT_CODE.OK:
            filter_conds, err_msg = format_model_query_conditions(self.model, filters=filters)
            if err_msg:
                result.code = RESULT_CODE.INVALID_PARAM
                result.message = err_msg
                break

            m = await DbProxy().find_item(self.model, filters=filter_conds)
            if m:
                result.code = RESULT_CODE.OK
                result.message = i18n.t('basic.success', **locale_params)
                if hasattr(m, 'as_dict'):
                    result.data = getattr(m, 'as_dict')()
                else:
                    result.data = {}
            break
        
        return result.encode_json()

