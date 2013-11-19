Title: Shut up and measure!
Date: 2013-10-09 19:57
Category: blog
Tags: python, decorator, profile

You probably have heard of the term *premature optimization*. It refers to writing "fast" code which is more obfuscated and (more often than not) slower than a straightforward approach --- before you have bothered to measure whether it really pays off to spend your cerebral CPU time (which is usually much more precious than its electronic counterpart) on such optimizations. It turns out that most of the time the bottleneck lurks in a place you would never have imagined, typically some primitive function call which just gets called a couple of zillion times.

For instance, I've been able to achieve speedups of productive code by factors of 2 and even 10 by identifying millions of database lookups --- each of them highly optimized --- and replacing that by some smarter algorithm like "fetch all relevant data in one query and only once". When confronted with the culprit, the seasoned programmer would usually be rather surprised. Trust me, 3 out of 4 programmers never measure and prefer drawing you into discussions on how to make this and that faster instead on how to make this work at all.

So how do you measure, then? As so often, the answer is in the standard library, in a module called [`profile`](http://docs.python.org/2/library/profile.html). What is missing for many people is to lower their activation energy by some convenient one-liner to rule all them functions. Enter the `@profiler` decorator:

``` python
import cProfile
import functools
import pstats

def profiler(filename):
    @functools.wraps(profiler)
    def _profiler(f):
        @functools.wraps(f)
        def __profiler(*args, **kwargs):
            profile = cProfile.Profile()
            result = profile.runcall(f, *args, **kwargs)
            profile.dump_stats(filename)
            return result
        return __profiler
    return _profiler
```

Using this decorator, it is straightforward to mostly eliminate the boilerplate code for --- and hence the lame excuses for not --- profiling virtually any piece of Python code:

``` python
def factorial(n):
    return n * factorial(n-1) if n else 1

profiled_factorial = profiler('/tmp/profile.txt')(factorial)
profiled_factorial(500)
```

This will write a binary raw profile to `/tmp/profile.txt`. I usually decorate a function fairly high in the hierarchy, something like a `main()` call, and I introduce some --- environment variable or command-line --- switch which enables profiling any time I wish. You will be amazed, it typically delivers the bottleneck right away.

But how do I extract human-readable information, then, I hear you ask? The short answer is: have a deeper look at the Python docs. Here is one quick-and-dirty way to get you going:

``` python
import cStringIO

def stats(filename, column, fraction):
    stream = cStringIO.StringIO()
    stats = pstats.Stats(filename, stream=stream)
    stats.strip_dirs().sort_stats(column).print_stats(fraction)
    return stream.getvalue()

print stats('/tmp/profile.txt', 'cumulative', 0.5)
```

which leads to the following tabular result:

```
Sat Oct 19 21:27:47 2013    /tmp/profile.txt

        502 function calls (2 primitive calls) in 0.001 seconds

  Ordered by: cumulative time
  List reduced from 2 to 1 due to restriction <0.5>

  ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   501/1    0.001    0.000    0.001    0.001 profiler.py:28(factorial)
```

In most cases I get away with pretty much this; the decorator I actually use also attaches the statistics with a fairly small fraction (say, 20%) to a variable `__stats__` on the decorated function so I can print that to a log file without much ado, and I have a little script onto which I can drag and drop binary profiles and obtain tabular report files in greater detail. Oh, and one last thing: don't bother profiling at all when your program is fast enough for your needs, and if you optimize, focus your work on the worst time consumer!

Now you are able to write code more quickly because whenever the devil in your ear starts telling you to "unroll this loop, then implement this in native C", the angel in your other ear will tell you to "shut up and write expressive and straightforward pythonic code". In the end you'll measure, tweak the bottlenecks, and you have written fast code quickly.

For the sake of completeness: There is a [patch](http://bugs.python.org/file29050/profile.patch) which was recently submitted to the standard library which delivers a similar functionality by means of a context manager. This is nice for debugging but a context manager is more difficult to toggle on and off by means of an external switch in productive code than a decorator.

``` python
import contextlib
import cProfile

@contextlib.contextmanager
def profiler(filename=None, sort=-1):
    prof = cProfile.Profile()
    prof.enable()
    try:
        yield
    finally:
        prof.disable()
    if filename is not None:
        prof.dump_stats(filename)
    else:
        result = prof.print_stats(sort)

with profiler():
	factorial(5)
```