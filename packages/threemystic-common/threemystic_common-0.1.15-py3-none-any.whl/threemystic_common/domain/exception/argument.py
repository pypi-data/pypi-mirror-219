import sys

from threemystic_common.domain.exception.base_class.base import exception_base as base


class exception_argument(base): 
  """This is a common set of methods and libraries"""

  def __init__(self, *args, **kwargs) -> None:
    if "exception_type" in kwargs:
      kwargs.pop("exception_type")
    super().__init__(
      exception_type = "argument", *args, **kwargs
    )
  
  
  