from threemystic_common.base_class.base import base as main_base

class base(main_base): 
  """This is a set of library wrappers to help general python apps"""

  def __init__(self, main_reference, logger_name, *args, **kwargs) -> None:
    self._main_reference= main_reference
    self._logger_name = logger_name

  
