Title: Round-robin scheme
Date: 2013-11-10 09:18
Category: blog
Tags: python, recipes, itertools, round-robin, sentinel

Since I already was at improving [`itertools`](http://docs.python.org/library/itertools.html) recipes in the [last post](/blog/2013/11/09/iterate-in-chunks/), there is a recipe for [round-robin consuming of iterables](http://docs.python.org/library/itertools.html#recipes) which can be written much more concise and yet --- to the functional programmer's eye --- more clearly:

``` python
from itertools import chain, izip_longest

def roundrobin(*iterables):
    sentinel = object()
    return (
        x for x in chain(*izip_longest(fillvalue=sentinel, *iterables))
        if x is not sentinel
    )
```

You also see a recipe for a "sentinel", that is, a unique value which helps to find the end of a sequence, filter out unneeded values, etc. People tend to use things such as `None` for this, but this way you never can be sure that this particular `None` you're coming across just now is not a non-sentinel. The simplest way to define a unique object is to instantiate an `object` (sic) and use the `is` comparison to identify it. A little test-drive confirms that it works as announced:

```
>>> list(roundrobin('ABC', 'D', 'EF'))
['A', 'D', 'E', 'B', 'F', 'C']
```
