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
from hawthorn.formvalidation.formutils import validate_form, save_form_fields
from hawthorn.valueobjects.resultcodes import RESULT_CODE
from hawthorn.valueobjects.responseobject import GeneralResponseObject, ListResponseObject

from .utils import format_model_query_conditions, dump_model_data, read_request_parameters, get_locale_params, get_listquery_pager_info, get_listquery_sort_info

LOG = logging.getLogger('services.generalmodelapi.apihandlers')

class ModelApiHandler():
    """
    Model API handler wrapper
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
                    result.data = dump_model_data(m)
            break
        
        return result.encode_json()

    async def handler_list(self, handler: GeneralTornadoHandler, request: tornado.httputil.HTTPServerRequest):
        """
        API handler of get model list data by filter condition and pagination
        """
        params = read_request_parameters(request)
        locale_params = get_locale_params(request)
        filters = params.get('filter', {})
        fields = params.get('fields', [])
        if not filters or not isinstance(filters, dict):
            filters = {}
        limit, offset = get_listquery_pager_info(params)
        orderby, direction = get_listquery_sort_info(params)

        result = ListResponseObject(RESULT_CODE.DATA_DOES_NOT_EXISTS, message=i18n.t('basic.data_not_exists', **locale_params))
        while result.code != RESULT_CODE.OK:
            filter_conds, err_msg = format_model_query_conditions(self.model, filters=filters)
            if err_msg:
                result.code = RESULT_CODE.INVALID_PARAM
                result.message = err_msg
                break

            rows, total = await DbProxy().query_list(self.model, filters=filter_conds, limit=limit, offset=offset, sort=orderby, direction=direction, selections=fields)
            
            if not fields:
                if hasattr(self.model, 'as_dict'):
                    formatted_rows = []
                    for row in rows:
                        m = self.model()
                        for k, v in row.items():
                            setattr(m, k, v)
                        formatted_rows.append(getattr(m, 'as_dict')())
                    rows = formatted_rows

            result.code = RESULT_CODE.OK
            result.message = i18n.t('basic.success', **locale_params)
            result.total = total
            result.data = rows
            if limit:
                result.pageSize = limit
                result.page = int(offset/limit) + 1
        return result.encode_json()

    async def handler_add(self, handler: GeneralTornadoHandler, request: tornado.httputil.HTTPServerRequest):
        """
        API handler of add model instance data
        """
        locale_params = get_locale_params(request)
        if not self.add_form:
            return '%s add form not configured for general add form handler, please specify add_form when register model general api handlers' % (get_model_class_name(self.model)), HTTPStatus.INTERNAL_SERVER_ERROR
        inputs = request_body_as_json(request)
        form_item = self.add_form(formdata=None, data=inputs, meta={ 'csrf': False })
        result = validate_form(form_item)
        if not result.is_success():
            return result.encode_json()

        m = self.model()
        if hasattr(m, 'set_session_uid'):
            session_uid = handler.session['user_id']
            setattr(m, 'set_session_uid', session_uid)
        save_form_fields(form_item, m, ignore_empty=True)

        result = GeneralResponseObject(code=RESULT_CODE.FAIL, message=i18n.t('basic.create_data_failed', **locale_params))
        try:
            res = await DbProxy().insert_item(m, auto_flush=True)
            if res:
                result.code = RESULT_CODE.OK
                result.message = i18n.t('basic.success', **locale_params)
                LOG.info('insert [%s] succeed', get_model_class_name(self.model))
            else:
                LOG.warning('insert [%s] failed', get_model_class_name(self.model))
        except Exception as e:
            LOG.error('insert [%s] failed with error:%s', get_model_class_name(self.model), str(e))
            result.code = RESULT_CODE.FAIL
            result.message = str(e)
        return result.encode_json()

    async def handler_edit(self, handler: GeneralTornadoHandler, request: tornado.httputil.HTTPServerRequest):
        """
        API handler of edit model instance data
        """
        locale_params = get_locale_params(request)
        if not self.edit_form:
            return '%s edit form not configured for general add form handler, please specify edit_form when register model general api handlers' % (get_model_class_name(self.model)), HTTPStatus.INTERNAL_SERVER_ERROR
        inputs = request_body_as_json(request)
        form_item = self.edit_form(formdata=None, data=inputs, meta={ 'csrf': False })
        result = validate_form(form_item)
        if not result.is_success():
            return result.encode_json()
        
        columns, pk = model_columns(self.model)
        form_pk_id = getattr(form_item, pk)
        m = await DbProxy().find_item(self.model, {getattr(self.model, pk)==form_pk_id})
        if not m:
            LOG.warning('get %s [%s] info failed while data does not extsts', get_model_class_name(self.model), str(form_pk_id))
            return GeneralResponseObject(code=RESULT_CODE.DATA_DOES_NOT_EXISTS, message=i18n.t('basic.data_not_exists', **locale_params)).encode_json()
        if hasattr(m, 'set_session_uid'):
            session_uid = handler.session['user_id']
            setattr(m, 'set_session_uid', session_uid)
        save_form_fields(form_item, m, ignore_empty=False)

        result = GeneralResponseObject(code=RESULT_CODE.FAIL, message=i18n.t('basic.edit_data_failed', **locale_params))
        try:
            res = await DbProxy().update_item(m)
            if res:
                result.code = RESULT_CODE.OK
                result.message = i18n.t('basic.success', **locale_params)
                LOG.info('edit %s [%s] succeed', get_model_class_name(self.model), str(form_pk_id))
            else:
                LOG.warning('edit %s [%s] failed', get_model_class_name(self.model), str(form_pk_id))
        except Exception as e:
            LOG.error('edit %s [%s] failed with error:%s', get_model_class_name(self.model), str(form_pk_id), str(e))
            result.code = RESULT_CODE.FAIL
            result.message = str(e)
        return result.encode_json()

    async def handler_delete(self, handler: GeneralTornadoHandler, request: tornado.httputil.HTTPServerRequest):
        """
        API handler of delete model instance data
        """
        inputs = request_body_as_json(request)
        locale_params = get_locale_params(request)
        columns, pk = model_columns(self.model)
        form_pk_id = inputs.get(pk, 0)
        if not form_pk_id:
            LOG.warning('delete %s while not giving any id to delete', get_model_class_name(self.model))
            return GeneralResponseObject(code=RESULT_CODE.INVALID_PARAM, message=i18n.t('basic.invalid_param', **locale_params)).encode_json()
        m = await DbProxy().find_item(self.model, {getattr(self.model, pk)==form_pk_id})
        if not m:
            LOG.warning('delete %s [%s] info failed while data does not extsts', get_model_class_name(self.model), str(form_pk_id))
            return GeneralResponseObject(code=RESULT_CODE.DATA_DOES_NOT_EXISTS, message=i18n.t('basic.data_not_exists', **locale_params)).encode_json()
        
        result = GeneralResponseObject(code=RESULT_CODE.FAIL, message=i18n.t('basic.delete_data_failed', **locale_params))
        try:
            res = False
            if False and hasattr(m, 'obsoleted'):
                if hasattr(m, 'set_session_uid'):
                    session_uid = handler.session['user_id']
                    setattr(m, 'set_session_uid', session_uid)
                setattr(m, 'obsoleted', 1)
                res = await DbProxy().update_item(m)
            else:
                res = await DbProxy().del_item(m)
            if res:
                result.code = RESULT_CODE.OK
                result.message = i18n.t('basic.success', **locale_params)
                LOG.info('delete %s [%s] succeed', get_model_class_name(self.model), str(form_pk_id))
            else:
                LOG.warning('delete %s [%s] failed', get_model_class_name(self.model), str(form_pk_id))
        except Exception as e:
            LOG.error('delete %s [%s] failed with error:%s', get_model_class_name(self.model), str(form_pk_id), str(e))
            result.code = RESULT_CODE.FAIL
            result.message = str(e)
        return result.encode_json()
