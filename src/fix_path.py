# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import google
import os

libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

# allow easy access to protobuf
google.__path__.append(os.path.join(libpath, 'google'))

# must come afterwards
from google.appengine.ext import vendor

# use our own lib directory
vendor.add(libpath)
