from threemystic_common.base_class.base_common import base


class app_monitoring_common(base): 
  """This is a common set of methods and libraries"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= "app_monitoring", *args, **kwargs)
  
  
  def performance(self, unset = False, *args, **kwargs):
    if(unset):
      self._unset("_performance")
      return
    
    if hasattr(self, "_performance"):
      return self._performance
    
    from threemystic_common.domain.app_monitoring.performance import \
        app_monitoring_performance as app_monitorin
    self._performance = app_monitorin(
      main_reference= self._main_reference
    )
    return self.performance(*args, **kwargs)
  