import functools

def check_for_name(func):
  @functools.wraps(func)
  def wrapper_function(*args, **kwargs):
    #insert code here
    return(
      func(
        *args, **kwargs
      )
    )

  return wrapper_function