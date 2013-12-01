Title: Named bitmap
date: 2013-11-15 19:16
Category: blog
Tags: namedtuple, bitmap, bin, python, recipes, closure, factory

Every now and then, one needs to keep track of a family of flags (boolean values), which you naturally would store in a numerical field which saves a lot of space and is database-friendly. Although the bit algrebra is straightforward, one often wishes to abstract that a little bit and to access the flags as attributes of some instance, pretty much like the awesome [`namedtuple`](http://docs.python.org/library/collections.html#collections.namedtuple) helps so much to clarify what entry 42 of that `tuple` was for again, in particular if some slot is being added or removed. So here it is:

<code data-gist-id="7506913" data-gist-file="bitmap.py"></code>

A little test run follows:

``` python
>>> test = bitmap('test', ['a', 'b', 'c'])
>>> t = test(5)
>>> t
test(0b101)
>>> t.a
True
>>> t.a = 0
>>> t
test(0b100)
>>> list(t)
[False, False, True]
>>> dict(zip(t.fields, t))
{'a': False, 'c': True, 'b': False}
```
