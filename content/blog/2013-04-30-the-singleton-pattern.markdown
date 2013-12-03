Title: The Singleton pattern
Date: 2013-04-30 23:00
Category: blog
Tags: python, design-pattern, singleton, multipleton, java, recipes

In this post I am going to discuss the [Singleton pattern](http://en.wikipedia.org/wiki/Singleton_pattern) in the Python context. Singleton is a [design pattern](http://en.wikipedia.org/wiki/Software_design_pattern) which addresses the problem that one often would like to have a single instance of some class, say, of a database connection pool or a logging facility. This instance is usually globally accessible. A prominent example is [`logging.getLogger()`](http://docs.python.org/2/library/logging.html#logging.getLogger)
in the Python standard library, which should rather be called a "multipleton" because it manages many instances but always returns the same instance for a given argument.

Please be warned: a singleton is just a (smart) global variable and therefore breaks encapsulation and unit-testability. So think at least twice whether there's no other way to solve your task. Having said that  you are well-advised to read the [Wikipedia article](http://en.wikipedia.org/wiki/Singleton_pattern) which will tell you quite a bit about the state of the debate and about Java implementations. Being a language for consenting adults, Python has no strict concept of private variables, so no Python implementation will ever truly prevent you from creating instances if you really want to. When I dug into the available Python [recipes](http://code.activestate.com/recipes/tags/singleton/) quite a while ago, I felt lost. In particular I was uncontent that many solutions were either not thread safe or not very reusable, or both.

If your object is cheap to create, you won't need lazy initialization. Module imports are thread safe, so you can get away with something as simple as

``` python
class singleton(object):
    pass
singleton = singleton()
```

Put this in a module of your choice, and the first thread to import that module will initialize your instance. This solution is so simple that reusability is not an issue. If you need something more advanced, this `@multipleton` decorator may be for you:

``` python
def multipleton(cls):
    import threading
    lock = threading.RLock()
    instances = {}

    def create(*args):
        with lock:
            try:
                return instances[args]
            except KeyError:
                instances[args] = instance = cls(*args)
                return instance

    return create
```
This solution is based upon [this recipe](http://code.activestate.com/recipes/578103-singleton-parameter-based/), but it adds thread safety, and I decided to drop the support for keyword arguments because they break uniqueness of the generated instances. I like this recipe for the following reasons:

* It is Pythonic and concise.
* It is generic and highly reusable.
* It supports lazy initialization in a thread safe manner.

A simple decorator function does the job without the need for a spurious parent or mixin class, or even metaclass magic. And it does the job even better: inheritance issues are avoided altogether, and it is also more flexible because it allows to "bless" any existing Python class.

A simple test run follows:

``` python
@multipleton
class A(object):
    def __init__(self, *args):
        import time
        time.sleep(0.01)

from multiprocessing.pool import ThreadPool
pool = ThreadPool(2)
results = [pool.apply_async(A) for _ in xrange(2)]
instances = set(r.get() for r in results)

print instances
```

You will see that there is only one instance, although two threads tried to create that instance concurrently. Observe what happens when you remove the line with the `with` statement.
