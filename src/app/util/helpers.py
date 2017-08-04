# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
import datetime
import hashlib
import itertools
import json
import re

from google.appengine.ext import ndb


def name2rgb(name=None):
    """Convert a string (spaces allowed) to an rgb value for consistent colors.

    Args:
        name: The string containing the name of an item

    Returns:
        (r, g, b) color triplet for use as a color for that item
    """
    if name is None:
        name = "Name"
    md5Name = hashlib.md5(name).hexdigest()
    return (int("0x" + md5Name[0:2], 0), int("0x" + md5Name[15:17], 0), int("0x" + md5Name[30:32], 0))


def parse_datetime(when=None):
    """Convert a string of YYYY-MM-DD HH:MM date to milliseconds since epoch.

    Args:
      when: The string containing the YYYY-MM-DD HH:MM format of the time or current UTC datetime if None.

    Returns:
      Integral number of milliseconds since epoch.
    """
    if when is None:
        when = when.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    dt_splits = re.sub('[- :]', '-', when).split('-')
    return datetime.datetime(int(dt_splits[0]), int(dt_splits[1]), int(dt_splits[2]), int(dt_splits[3]),
                             int(dt_splits[4]))


def parse_date(date=None):
    """Convert a string of YYYY-MM-DD date to milliseconds since epoch.

    Args:
      date: The string containing the YYYY-MM-DD format of the time or current UTC date if None.

    Returns:
      Integral number of milliseconds since epoch.
    """
    if date is None:
        date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    date_splits = date.split('-')
    return datetime.datetime(int(date_splits[0]), int(date_splits[1]), int(date_splits[2]))


def to_date(when):
    """Convert a number of milliseconds since epoch to a string with the date.

    Args:
      when: The number of milliseconds since epoch.

    Returns:
      A String in the format YYYY-MM-DD
    """
    return datetime.datetime.utcfromtimestamp(float(when) / 1000.0).strftime('%Y-%m-%d')


def to_datetime(when):
    """Convert a number of milliseconds since epoch to a string with the datetime in proper format.

    Args:
      when: The number of milliseconds since epoch.

    Returns:
      A String in the format YYYY-MM-DD HH:MM
    """
    return datetime.datetime.utcfromtimestamp(float(when) / 1000.0).strftime('%Y-%m-%d %H:%M')


def to_us(when=None):
    """Convert a datetime instance to microseconds since epoch.

    Args:
      when: The datetime instance to convert, or current UTC datetime if None.

    Returns:
      Integral number of microseconds since epoch.
    """
    if when is None:
        when = datetime.datetime.utcnow()
    return long((calendar.timegm(when.timetuple()) * 1000000) + when.microsecond)


def from_us(when):
    """Convert a number of microseconds since epoch to a UTC datetime instance.

    Args:
      when: The number of microseconds since epoch.

    Returns:
      A datetime instance in UTC.
    """
    # TODO: test this around timezone changes etc?
    return datetime.datetime.utcfromtimestamp(float(when) / 1000000.0)


def to_ms(when=None):
    """Convert a datetime instance to milliseconds since epoch.

    Args:
      when: The datetime instance to convert, or current UTC datetime if None.

    Returns:
      Integral number of milliseconds since epoch.
    """
    return long(to_us(when) / 1000)


def from_ms(when):
    """Convert a number of milliseconds since epoch to a UTC datetime instance.

    Args:
      when: The number of milliseconds since epoch.

    Returns:
      A datetime instance in UTC.
    """
    # TODO: test this around timezone changes etc?
    return datetime.datetime.utcfromtimestamp(float(when) / 1000.0)


def grouper(n, iterable):
    """Allow iteration over an iterable in chunks of a defined size.

    Args:
      n: Chunk size.
      iterable: The base iterable to group into chunks.

    Yields:
      A tuple containing at most n items from the iterable.
    """
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def slugify(words):
    """Convert an input string into a URL-safe form, suitable for use as a "slug".

    A slug can only contain the basic alphanumeric characters (no accents) and a
    dash. Disallowed characters are converted to dashes, runs of dashes are
    reduced to a single element, and dashes at the start or end are removed.

    Args:
      words: The input to convert

    Returns:
      The slugified string.
    """
    words = words.lower()
    words = re.sub(r'[^0-9a-zA-Z-]+', '-', words)
    words = re.sub(r'^-+', '', words)
    words = re.sub(r'-+$', '', words)
    return words


class JSONEncoder(json.JSONEncoder):
    """Special subclass of json.JSONEncoder to handle serialization of additional
    types."""

    def default(self, o):
        if hasattr(o, 'to_hash'):
            return o.to_hash()
        if hasattr(o, 'to_dict'):
            return o.to_dict()
        if isinstance(o, ndb.Key):
            return None
        if isinstance(o, set):
            return list(o)
        if isinstance(o, ndb.GeoPt):
            return {'longitude': o.lon, 'latitude': o.lat}
        if hasattr(o, 'timetuple') and hasattr(o, 'microsecond'):
            # datetime-like
            return to_ms(o)
        if type(o).__name__ == '_BaseValue':
            return o.b_val

        return super(JSONEncoder, self).default(o)


def json_encode(data, stream=None, **kwargs):
    if stream:
        json.dump(data, stream, separators=(',', ':'), cls=JSONEncoder, **kwargs)
    else:
        return json.dumps(data, separators=(',', ':'), cls=JSONEncoder, **kwargs)
