# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import uuid

from google.appengine.api import modules
from google.appengine.api import taskqueue

from app.util.helpers import json_encode, to_ms


def _get_target():
    version_name = modules.get_current_version_name()
    if version_name in ('prod', 'm', 'api', 'batchops', 'mapreducer'):
        return 'batchops'
    return version_name


class TaskBuilder(object):
    @staticmethod
    def _new_task(url, **kwargs):
        kwargs.setdefault('target', _get_target())
        return taskqueue.Task(
            name=kwargs.get('name', uuid.uuid4().hex),
            url=url,
            **kwargs
        )

    @classmethod
    def log_params(cls, **kwargs):
        return cls._new_task(
            '/_tasks/util/log_params',
            params=kwargs,
        )

    @classmethod
    def log_trace(cls, data, **kwargs):
        kwargs.setdefault('trace_data', data if isinstance(data, basestring) else
        json.dumps(data))
        return cls._new_task(
            '/_tasks/util/log_trace',
            params=kwargs,
        )