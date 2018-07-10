# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import logging

from google.appengine.api import memcache
from google.appengine.ext import ndb

from . import enums

GuidSuffix = enums.enum(
	THOBJECT='1',
)


class AutoUuidProperty(ndb.TextProperty):
	_truncated = False

	_attributes = ndb.TextProperty._attributes + ['_truncated']

	def __init__(self, name=None, truncated=None, **kwds):
		super(AutoUuidProperty, self).__init__(name=name, **kwds)
		self._truncated = bool(truncated)

	def _prepare_for_put(self, entity):
		if not self._retrieve_value(entity):
			value = uuid.uuid4().hex
			if self._truncated:
				value = value[0:16]
			self._store_value(entity, value)


class GuidProperty(ndb.TextProperty):
	_suffix = False

	_attributes = ndb.TextProperty._attributes + ['_suffix']

	def __init__(self, name=None, suffix=None, **kwds):
		super(GuidProperty, self).__init__(name=name, **kwds)
		self._suffix = suffix
		if not suffix:
			raise ValueError('GuidProperty %s must have a suffix.' % self._name)
		if not isinstance(suffix, basestring):
			raise ValueError('GuidProperty %s suffix must be a string.' %
							 self._name)

	def _prepare_for_put(self, entity):
		if not self._has_value(entity):
			value = '%s.%s' % (uuid.uuid4().hex, self._suffix)
			self._store_value(entity, value)


class BaseModel(ndb.Model):
	pass


class AutoUuidModel(BaseModel):
	def __init__(*args, **kwds):
		# self is passed implicitly through args so users can define a property
		# named 'self'.
		(self,) = args
		args = args[1:]
		super(AutoUuidModel, self).__init__(*args, **kwds)
		if not self._properties or 'uuid' not in self._properties:
			raise TypeError('A "uuid" property must be defined for the %s model' %
							self.__class__.__name__)
		# force UUID generation to happen on model instance creation
		self._properties['uuid']._prepare_for_put(self)

	@classmethod
	def fetch_by_uuid(cls, uuid):
		return cls.get_by_id(uuid)

	def _prepare_for_put(self):
		# prepare properties, which will definitely populate the UUID
		super(AutoUuidModel, self)._prepare_for_put()
		# use the UUID as the key
		if self._key is None:
			self._key = ndb.Key(self._get_kind(), self.uuid)


class GuidModel(BaseModel):
	def __init__(*args, **kwds):
		# self is passed implicitly through args so users can define a property
		# named 'self'.
		(self,) = args
		args = args[1:]
		super(GuidModel, self).__init__(*args, **kwds)
		if not self._properties or 'guid' not in self._properties:
			raise TypeError('A "guid" property must be defined for the %s model' %
							self.__class__.__name__)
		# force GUID generation to happen on model instance creation
		self._properties['guid']._prepare_for_put(self)

	@classmethod
	def fetch_by_guid(cls, guid):
		# return cls.get_by_id(guid)
		data = memcache.get(guid)
		if data is None:
			data = cls.get_by_id(guid)
			memcache.add(guid, data)
		return data

	def _prepare_for_put(self):
		# prepare properties, which will definitely populate the GUID
		super(GuidModel, self)._prepare_for_put()
		# use the GUID as the key
		if self._key is None:
			self._key = ndb.Key(self._get_kind(), self.guid)

	def _post_put_hook(self, future):
		super(GuidModel, self)._post_put_hook(future)
		if not memcache.set(self.guid, self):
			memcache.add(self.guid, self)
