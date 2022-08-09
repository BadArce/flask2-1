from decorators import check_for_name, only_strings

@check_for_name
def print_my_name(greeting, my_name):
  print("----------print_my_name()")
  print(f"{greeting}, {my_name}")

@only_strings
def concat(a,b,c):
  result = a + b + c
  print(result)
  return result