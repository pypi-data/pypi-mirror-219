from threemystic_common.base_class.base_common import base


class exception_common(base): 
  """This is a common set of methods and libraries"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= "exception", *args, **kwargs)

    from threemystic_common.domain.exception.generic import exception_generic as exception
    self._exception = {
      "generic": exception
    }
  
  # https://docs.python.org/3/library/exceptions.html
  def _custom_exceptions(self):
    return [
      "argument",
      "function"
    ]

  def exception(self, exception_type, *args, **kwargs):
    
    if self._main_reference.helper_type().string().is_null_or_whitespace(exception_type):
      return self._exception.get("generic")

    exception_type = exception_type.lower()
    if exception_type not in self._custom_exceptions():
      return self._exception.get("generic")(main_reference= self._main_reference, exception_type= exception_type, *args, **kwargs)
    
    if exception_type == "argument":
      if self._exception.get(exception_type):
        return self._exception[exception_type](main_reference= self._main_reference, exception_type= exception_type, *args, **kwargs)
      
      from threemystic_common.domain.exception.argument import exception_argument as exception
      self._exception[exception_type] = exception
      return self.exception(exception_type= exception_type, *args, **kwargs)
    
    if exception_type == "function":
      if self._exception.get(exception_type):
        return self._exception[exception_type](main_reference= self._main_reference, exception_type= exception_type, *args, **kwargs)
      
      from threemystic_common.domain.exception.function import exception_function as exception
      self._exception[exception_type] = exception
      return self.exception(exception_type= exception_type, *args, **kwargs)
    