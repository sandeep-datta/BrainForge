import functools

def printargs(func):
   def wrapper(*args, **kwargs):
      strargs = strkwargs = ""
      if args:
         strargs = ", ".join([repr(a) for a in args])
      
      if kwargs:
         strkwargs = ", ".join(["=".join([repr(a) for a in x]) for x in kwargs.items()])
      
      if args and kwargs:
         print("%s(%s, %s)" % (func.__name__, strargs, strkwargs))
      elif args or kwargs:
         print("%s(%s)" % (func.__name__, strargs or strkwargs)) #the or operator returns the argument which is true
      else:
         print("%s()" % (func.__name__))

      return func(*args, **kwargs)
   return wrapper

class memoized(object):
   """Decorator that caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned, and
   not re-evaluated.
   """
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args, **kwarg):
      key = args + tuple((x for i in kwarg.items() for x in i)) #Flatten keyword args into a list
      try:
         return self.cache[key]
      except KeyError:
         value = self.func(*args, **kwarg)
         self.cache[key] = value
         return value
      except TypeError:
         # uncachable -- for instance, passing a list as an argument.
         # Better to not cache than to blow up entirely.
         return self.func(*args, **kwarg)

   def __repr__(self):
      """Return the function's docstring."""
      return self.func.__doc__
   def __get__(self, obj, objtype):
      """Support instance methods."""
      return functools.partial(self.__call__, obj)

# @memoized
# @printargs
# def fibonacci(n, **kwargs):
#    "Return the nth fibonacci number."
#    if n in (0, 1):
#       return n
#    return fibonacci(n-1) + fibonacci(n-2)


# @memoized
# @printargs
# def test(*args, **kwargs):
#    pass
#    