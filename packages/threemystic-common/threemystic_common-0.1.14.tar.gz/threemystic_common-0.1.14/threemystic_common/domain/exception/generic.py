import sys

from threemystic_common.domain.exception.base_class.base import exception_base as base


class exception_generic(base): 
  """This is a common set of methods and libraries"""

  def __init__(self, main_reference, *args, **kwargs) -> None:
    super().__init__(
      main_reference= main_reference, *args, **kwargs
    )
  
  