from threemystic_common.base_class.base_common import base


class exception_base(base): 
  """This is a set of library wrappers to help create a cmdb"""

  def __init__(self, exception_type = "generic", *args, **kwargs) -> None:
    super().__init__(logger_name= f"exception_{exception_type}", *args, **kwargs)
    self._exception_type = exception_type.lower()

  def exception(self, message, name = None, logger = None, exception = None, *args, **kwargs):
    if logger is None:
      logger = self._main_reference.get_logger()

    if name is not None and self._exception_type != "generic":
      return_exception = Exception(f"{self._exception_type}: {name}\n{message}")
      logger.exception(
        msg= str(return_exception),
        extra =  {
          "main_exception": return_exception,
          "inner_exception": exception
        }
      )
      return return_exception
    
    if name is not None:
      return_exception = Exception(f"{name}\n{message}")
      logger.exception(
        msg= str(return_exception),
        extra =  {
          "main_exception": return_exception,
          "inner_exception": exception
        }
      )
      return return_exception
    
    return_exception =Exception(message)
    logger.exception(
      msg= str(return_exception),
      extra =  {
        "main_exception": return_exception,
        "inner_exception": exception
      }
    )
    return return_exception

  def not_implemented(self, message, name = None, logger = None, exception = None, *args, **kwargs):
    if logger is None:
      logger = self._main_reference.get_logger()
    if name is not None and self._exception_type != "generic":
      return_exception = NotImplementedError(f"{self._exception_type}: {name}\n{message}")
      logger.exception(
        msg= str(return_exception),
        extra =  {
          "main_exception": return_exception,
          "inner_exception": exception
        }
      )
      return return_exception
    
    if name is not None:
      return_exception = NotImplementedError(f"{name}\n{message}")
      logger.exception(
        msg= str(return_exception),
        extra =  {
          "main_exception": return_exception,
          "inner_exception": exception
        }
      )
      return return_exception
    
    return_exception =NotImplementedError(message)
    logger.exception(
      msg= str(return_exception),
        extra =  {
          "main_exception": return_exception,
          "inner_exception": exception
        }
    )
    return return_exception
  
  def type_error(self, message, name = None, logger = None, exception = None, *args, **kwargs):
    if logger is None:
      logger = self._main_reference.get_logger()
    if name is not None and self._exception_type != "generic":
      return_exception = TypeError(f"{self._exception_type}: {name}\n{message}")
      logger.exception(
        msg= str(return_exception),
        extra =  {
          "main_exception": return_exception,
          "inner_exception": exception
        }
      )
      return return_exception
    
    if name is not None:
      return_exception = TypeError(f"{name}\n{message}")
      logger.exception(
        msg= str(return_exception),
        extra =  {
          "main_exception": return_exception,
          "inner_exception": exception
        }
      )
      return return_exception
    
    return_exception =TypeError(message)
    logger.exception(
      msg= str(return_exception),
      extra =  {
        "main_exception": return_exception,
        "inner_exception": exception
      }
    )
    return return_exception
  
  def key_error(self, message, name = None, logger = None,  exception = None,*args, **kwargs):
    if logger is None:
      logger = self._main_reference.get_logger()
    if name is not None and self._exception_type != "generic":      
      return_exception = KeyError(f"{self._exception_type}: {name}\n{message}")
      logger.exception(
        msg= str(return_exception),
        extra =  {
          "main_exception": return_exception,
          "inner_exception": exception
        }
      )
      return return_exception
    
    if name is not None:
      return_exception = KeyError(f"{name}\n{message}")
      logger.exception(
        msg= str(return_exception),
        extra =  {
          "main_exception": return_exception,
          "inner_exception": exception
        }
      )
      return return_exception
    
    return_exception =KeyError(message)
    logger.exception(
      msg= str(return_exception),
      extra =  {
        "main_exception": return_exception,
        "inner_exception": exception
      }
    )
    return return_exception