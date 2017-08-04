# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

import webapp2
from webapp2_extras import jinja2

from app.util.template_filters import FILTERS
from app.util.helpers import name2rgb

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(
	os.path.dirname(os.path.realpath(__file__)))), 'tpl')

LOCALE_DIR = os.path.join(os.path.dirname(os.path.dirname(
	os.path.dirname(os.path.realpath(__file__)))), 'locale')


def jinja2_factory(app):
	j2_config = {
		'template_path': TEMPLATE_DIR,
		'translations_path': LOCALE_DIR,
		'environment_args': {
			'auto_reload': False,
			'cache_size': 400,
			'extensions': [
				'jinja2.ext.autoescape',
				'jinja2.ext.do',
				'jinja2.ext.with_',
				'jinja2.ext.i18n',
			],
			'trim_blocks': True,
		},
		'filters': FILTERS,
		'globals': {
			'uri_for': webapp2.uri_for,
			'now': datetime.datetime.now(),
			'getattr': getattr,
			'len': len,
			'enumerate': enumerate,
			'name2rgb': name2rgb,
		}
	}
	return jinja2.Jinja2(app, config=j2_config)


def get_jinja2(app=None):
	return jinja2.get_jinja2(factory=jinja2_factory, app=app)
