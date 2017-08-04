# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from google.appengine.ext import vendor
import os

# Horrible hack to work around App Engine restrictions
os.path.expanduser = lambda x: x
import logging
from google.appengine.api import logservice

logservice.AUTOFLUSH_EVERY_SECONDS = None
# logservice.AUTOFLUSH_EVERY_BYTES = None
logservice.AUTOFLUSH_EVERY_LINES = 10

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
