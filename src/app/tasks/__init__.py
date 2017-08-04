# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from app.util import request


class RequestHandler(request.RequestHandler):
	def enforce_ssl(self):
		pass

	def fetch_user(self):
		pass

	def log_user_info(self):
		pass


class NotFound(RequestHandler):
	"""Simple "not found" handler. Used as a catchall."""

	def get(self, *args, **kwargs):
		self.abort_not_found()

	def post(self, *args, **kwargs):
		self.abort_not_found()


class LogParams(RequestHandler):
	def post(self, *args, **kwargs):
		for k in self.request.POST.keys():
			logging.debug("%s: %r", k, self.request.POST[k])
