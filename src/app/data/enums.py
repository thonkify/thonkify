import collections


def enum(*sequential, **named):
    enums = collections.OrderedDict(zip(sequential, sequential), **named)
    _keys = enums.keys()
    _values = enums.values()
    enums.update({'_keys': _keys, '_values': _values})
    return type(r'Enum', (), enums)


Shared = enum('GLOBAL', 'WORKSPACE_SPECIFIC')
