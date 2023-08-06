import copy
from threemystic_common.base_class.base_common import base


class helper_type_general(base): 
  """This is a set of general type helpers"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_type_general", *args, **kwargs)
  
  def is_integer(self, n):
    try:
      if(self.is_numeric(n)):
        float(n)
    except ValueError:
      return False
    else:
      return float(n).is_integer()
  
  def is_numeric(self, n, *args, **kwargs):
    try:
      return str(n).isnumeric()
    except:
      return False
  
  def is_type(self, obj, type_check, *args, **kwargs):
    if isinstance(type_check, list):
      for check in type_check:
        if self.is_type(obj= obj, type_check= check):
          return True
      return False
    try:
      return isinstance(obj, type_check)
    except:
      return type(obj) == type_check
  
  def get_type(self, obj, *args, **kwargs):
    return type(obj)
  
  def if_null_default(self, check_val, default_val, enforce_type = None, *args, **kwargs):
    if enforce_type is not None and not self.is_type(check_val, enforce_type):
      return default_val

    if check_val is None:
      return default_val
    
    return check_val
  
  def copy_object(self, object_copy, deep_copy = True, *args, **kwargs):
    if object_copy is None:
      return None

    if deep_copy:
      return copy.deepcopy(object_copy)
    
    return copy.copy(object_copy)
  
  

  def get_container_value(self, container, value_key, *args, **kwargs):
    if self.get_common().helper_type().general().is_type(value_key, str):
      if hasattr(container, value_key):
        return getattr(container, value_key)
      if value_key in container:
        return container[value_key]
      
      return None
    
    if not self.get_common().helper_type().general().is_type(value_key, list):
      raise self.get_common().exception().exception(
        exception_type = "argument"
      ).not_implemented(
        logger = self.get_common().get_logger(),
        name = "value_key",
        message = f"value_key must be either a string or an array. Got Type: {type(value_key)}"
      )
    
    if len(value_key) < 1:
      return None
    
    for key_value in value_key:
      container = self.get_container_value(container= container, value_key= key_value, *args, **kwargs)
      if container is None:
        return container

    return container