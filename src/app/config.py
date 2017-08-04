"""Core configuration for the app.
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import os

import webapp2
from google.appengine.api import memcache
from google.appengine.ext import ndb

##############################################################################
# You MUST change these settings if you run your own instance.
##############################################################################

# Google Analytics tracking ID.
ANALYTICS_ID = 'UA-104080797-1'

##############################################################################
# You should never need to modify these settings. They infer their values
# from the current environment.
##############################################################################

DEV_SERVER = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
STAGING_SERVER = 'staging' in os.environ.get('SERVER_NAME', 'localhost')
UNSTABLE_SERVER = 'unstable' in os.environ.get('SERVER_NAME', 'localhost')

# Whether we are in debug mode, or running on the local development server
DEBUG = DEV_SERVER or STAGING_SERVER or UNSTABLE_SERVER

# Base URL domain. MUST BE CHANGED.
BASE_DOMAIN = os.environ.get('SERVER_NAME', 'localhost')

# Base URL
BASE_URL = 'https://%s' % BASE_DOMAIN

# Whether to record AppStats (annoying on the dev server)
GAE_APP_STATS = not DEV_SERVER

# Whether to record Datastore stats (annoying on the dev server)
DATASTORE_STATS = True  # not DEV_SERVER

SETTING_MC_PREFIX = 'app.config.staging:' if STAGING_SERVER else 'app.config:'

##############################################################################
# These settings are managed by scripts and MUST NOT be manually modified.
##############################################################################

# Server version code
SERVER_VERSION = 'DEVELOPMENT'

##############################################################################
# The default values for all runtime-tweakable settings. This also provides
# the list for the admin console. Do not remove any!
##############################################################################

TWEAKABLE_DEFAULTS = {
}


class GlobalSetting(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    value = ndb.StringProperty(indexed=False)
    updated = ndb.DateTimeProperty(indexed=False)

    @classmethod
    def get(cls, name, default=None):
        setting = cls.get_by_id(name)
        if setting is None:
            return default
        return json.loads(setting.value)

    @classmethod
    def set(cls, name, value):
        setting = cls.get_by_id(name)
        if setting is None:
            setting = cls(
                id=name,
                name=name,
                value=None
            )
        setting.value = json.dumps(value)
        setting.updated = datetime.datetime.utcnow()
        setting.put()


def _update_caches(setting, value, skip_memcache=False):
    # Save to request-local cache
    request = webapp2.get_request()
    if request:
        if 'thonkify_setting_cache' not in request.registry:
            request.registry['thonkify_setting_cache'] = {}
        request.registry['thonkify_setting_cache'][setting] = value

    if not skip_memcache:
        # Save to memcache
        memcache.set('%s%s' % (SETTING_MC_PREFIX, setting), value)

    return value


def get_default(setting):
    if setting in TWEAKABLE_DEFAULTS:
        s = TWEAKABLE_DEFAULTS[setting]
        return s[0] if isinstance(s, tuple) else s
    raise KeyError('Setting "%s" does not exist' % setting)


def get(setting):
    # 1. Try request-local cache
    request = webapp2.get_request()
    if request:
        if 'thonkify_setting_cache' not in request.registry:
            request.registry['thonkify_setting_cache'] = {}
        if setting in request.registry['thonkify_setting_cache']:
            # NOTE: we don't update caches here because that's the only place it
            # could have come from, and it would result in a bunch of memcache set()
            # traffic.
            return request.registry['thonkify_setting_cache'][setting]

    # 2. Try memcache
    mc = memcache.get_multi([setting], key_prefix=SETTING_MC_PREFIX)
    if setting in mc:
        # ... but don't try to update memcache, because we've just got it from there
        return _update_caches(setting, mc[setting], skip_memcache=True)

    # 3. Try datastore
    value = GlobalSetting.get(setting)
    if value is not None:
        return _update_caches(setting, value)

    # 4. Fall back to defaults
    if setting in TWEAKABLE_DEFAULTS:
        s = TWEAKABLE_DEFAULTS[setting]
        return _update_caches(setting, s[0] if isinstance(s, tuple) else s)

    # 5. Module-level constant?
    if setting[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and setting in globals():
        return _update_caches(setting, globals()[setting])

    # 6. Give up
    raise KeyError('Setting "%s" does not exist' % setting)


def get_all():
    # 1. Start with defaults
    keys = list(TWEAKABLE_DEFAULTS.keys())

    # 3. Merge from memcache
    mc = memcache.get_multi(keys, key_prefix=SETTING_MC_PREFIX)
    result = {}
    for setting in keys:
        if setting in mc:
            result[setting] = (mc[setting], TWEAKABLE_DEFAULTS[setting][1])
        else:
            result[setting] = TWEAKABLE_DEFAULTS[setting]

    # 4. Merge from request-local cache
    request = webapp2.get_request()
    if request:
        if 'thonkify_setting_cache' not in request.registry:
            request.registry['thonkify_setting_cache'] = {}
        request.registry['thonkify_setting_cache'].update({k: v[0] for k, v in result.iteritems()})

    return result


def set(setting, value):
    if setting not in TWEAKABLE_DEFAULTS:
        raise KeyError('Setting "%s" does not exist' % setting)

    # Save to request-local cache and memcache
    _update_caches(setting, value)

    # Save to datastore
    GlobalSetting.set(setting, value)
