from threemystic_common.base_class.base_common import base
from math import pow
from time import sleep

class helper_type_requests(base): 
  """This is a set of library wrappers to help around expending int libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_type_requests", *args, **kwargs)
  
  def expodential_backoff_wait(self, attempt, max_wait = 30, auto_sleep = True, *args, **kwargs):
    back_off_time = pow(2, attempt)
    if back_off_time > max_wait:
      back_off_time = max_wait
    
    if auto_sleep:
      sleep(back_off_time)
      
    return back_off_time