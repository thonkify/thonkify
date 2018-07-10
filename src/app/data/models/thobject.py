import datetime
import logging
import sys
import traceback

from google.appengine.api import search, memcache
from google.appengine.ext import ndb

from app import config
from app.data import GuidModel, GuidProperty, GuidSuffix, enums

class Thobject(GuidModel):
    guid = GuidProperty(suffix=GuidSuffix.THOBJECT)
    workspace = ndb.StringProperty(indexed=True, default=None)
    shared_to = ndb.StringProperty(indexed=True, choices=enums.Shared._values, default=enums.Shared.WORKSPACE)
    keyword = ndb.StringProperty(indexed=True, default=None)
    original_poster = ndb.StringProperty(indexed=False, default=None)
    body = ndb.TextProperty(default=None)

    @classmethod
    def fetch_by_workspace_and_keyword(cls, workspace, keyword):
        #check workspace first
        thobject = cls.query(cls.workspace == workspace, cls.keyword == keyword).fetch(keys_only=True)

        if thobject:
            return ndb.get(thobject)

        #check all shared properties next
        thobject = cls.query(cls.keyword == keyword).fetch(keys_only=True)
        if thobject:
            return ndb.get(thobject)

        return None