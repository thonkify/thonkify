# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import functools

from google.appengine._internal.django.template import defaultfilters


def wrap_filter(f):
	@functools.wraps(f)
	def wrapped(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except AssertionError:
			# force-initialize old templates
			from google.appengine.ext.webapp import template
			import os
			template.render(os.path.join('tpl', '_blank.html'), {})
			return f(*args, **kwargs)

	return wrapped


FILTERS = {
	'date': wrap_filter(defaultfilters.date),
	'pluralize': wrap_filter(defaultfilters.pluralize),
	'timesince': wrap_filter(defaultfilters.timesince),
	'timeuntil': wrap_filter(defaultfilters.timeuntil),
}
