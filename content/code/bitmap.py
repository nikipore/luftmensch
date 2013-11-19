def bitmap(typename, fields):
    _fields = tuple(fields)
    _bits = dict((field, 2 ** j) for (j, field) in enumerate(_fields))
    _max = sum(_bits.itervalues())
    def _bit(field):
        try:
            return _bits[field]
        except KeyError:
            raise AttributeError('no such field: %s' % field)

    class _bitmap(object):
        def __init__(self, value=0):
            value = int(value)
            if not (0 <= value <= _max):
                raise ValueError('value not in range: %d' % value)
            self._value = value

        def __setattr__(self, field, value):
            if field == '_value':
                object.__setattr__(self, field, value)
                return
            bit = _bit(field)
            if value:
                self._value |= bit
            else:
                self._value &= (~bit)

        def __getattr__(self, field):
            return bool(_bit(field) & self._value)

        def __delattr__(self, field):
            setattr(self, field, False)

        def __eq__(self, other):
            return int(self) == int(other)

        def __index__(self):
            return int(self)

        def __iter__(self):
            for field in _fields:
                yield getattr(self, field)

        def __int__(self):
            return self._value

        def __repr__(self):
            return '%s(%s)' % (typename, self)

        def __str__(self):
            return bin(self)

    _bitmap.fields = _fields
    _bitmap.max = _max
    _bitmap.__name__ = typename
    return _bitmap
