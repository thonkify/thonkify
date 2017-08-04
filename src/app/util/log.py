# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging as orig_logging
import re

# copy attributes from the logging module, so we act exactly the same, probably


debug = orig_logging.debug
info = orig_logging.info
warning = orig_logging.warning
error = orig_logging.error
exception = orig_logging.exception


def tagged(tag, message, *args):
	if len(args):
		message %= tuple(args)
	orig_logging.info(':%s:=%s', tag, message)


def parse_tagged(message):
	"""Returns either None or a 2-tuple of (tag, value) from a tagged message."""
	m = re.match(r'^:([^:]+):=(.*)$', message)
	if not m:
		return None
	return m.groups()


def extract_tagged(messages):
	"""Returns a dict mapping tags to values from an iterable of tagged messages.

	If a tag is repeated, its value from the last message is returned.
	"""
	result = {}
	for m in messages:
		data = parse_tagged(m)
		if data:
			result[data[0]] = data[1]
	return result
