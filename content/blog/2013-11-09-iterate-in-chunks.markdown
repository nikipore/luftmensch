Title: Iterate in chunks
Date: 2013-11-09 09:07
Category: blog
Tags: python, itertools, chunks, iterator, recipes

A common idion is to consume an iterable in chunks. There is a [whole lot of ways to do it](http://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks), but most of them are either a bit clumsy, or they return the chunks in a non-lazy fashion, which breaks the generator idiom. There is even a [recipe](http://docs.python.org/library/itertools.html#recipes) in the standard documentation of the [`itertools`](http://docs.python.org/library/itertools.html) module which is still the best I could find:

``` python
from itertools import izip_longest

def chunks(iterable, size, fillvalue=None):
    return izip_longest(fillvalue=fillvalue, *([iter(iterable)] * size))
```

This one very clever and as concise at it gets. It has some drawbacks, though:

1. It breaks with the "be explicit rather than implicit" rule by composing the already quite advanced [transposition trick](blog/2013/10/09/how-to-transpose-a-matrix/) with a round-robin scheme on one and the same iterator.
2. The chunks are not "lazy" generators but tuples.
2. It requires fill values which to my use cases do more harm than good.

Thus, I'd like to add my own two cents here. In order to be lazy and avoid fill values, you need to peek whether the iterator is already exhausted:

``` python
from itertools import chain, islice

def chunks(iterable, size):
    iterable = iter(iterable)
    while True:
        yield chain([next(iterable)], islice(iterable, size - 1))
```

This is `chunks()` in action:

``` python
>>> for chunk in chunks(range(9), size=5):
...     print list(chunk)
...
[0, 1, 2, 3, 4]
[5, 6, 7, 8]
```