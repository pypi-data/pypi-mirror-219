#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import Form
from hawthorn.modelutils import ModelBase

class Relations:
    def __init__(self, src_field: str, dst_field: str, src_model: ModelBase, dst_model: ModelBase):
        self.src_field = src_field
        self.dst_field = dst_field
        self.src_model = src_model
        self.dst_model = dst_model

class _RESTfulAPIWraper:
    def __init__(self, endpoint: str, cls: ModelBase, add_form: Form = None, update_form: Form = None, relations: Relations = None):
        self.endpoint = endpoint
        self.cls = cls
        self.add_form = add_form
        self.update_form = update_form
        self.relations = relations
