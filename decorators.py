import functools

def check_for_name(func):
  @functools.wraps(func)
  def wrapper_function(*args, **kwargs):
    args = args[0:1]
    kwargs['my_name'] = ''
    return(
      func(
        *args, **kwargs
      )
    )

  return wrapper_function

def only_strings(func):
  @functools.wraps(func)
  def wrapper_function(*args, **kwargs):
    newargs = []
    for arg in args:
      newargs.append(str(arg))
    print(newargs)
    return(
      func(
        *newargs
      )
    )

  return wrapper_function