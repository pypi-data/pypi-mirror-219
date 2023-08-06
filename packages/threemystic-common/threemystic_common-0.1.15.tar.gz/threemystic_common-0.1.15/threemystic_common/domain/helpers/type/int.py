from threemystic_common.base_class.base_common import base


class helper_type_int(base): 
  """This is a set of library wrappers to help around expending int libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_type_int", *args, **kwargs)
  
  def get(self, int_value, default = None, *args, **kwargs):
    try:
      return int(int_value)
    except:
      return default