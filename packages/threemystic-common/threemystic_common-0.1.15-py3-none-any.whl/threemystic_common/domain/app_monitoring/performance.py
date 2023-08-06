from threemystic_common.base_class.base_common import base


class app_monitoring_performance(base): 
  """This is a set of library wrappers to help monitor performance"""

  def __init__(self, features, *args, **kwargs) -> None:
    super().__init__(logger_name= "app_monitoring_performance", *args, **kwargs)
    
    if features is None:
      return
    
    self.__enable_feature_memory(
      features= features, **kwargs
    )
  
  def __enable_feature_memory(self, features, **kwargs):
    if features.get("memory") == True:
      if hasattr(self, "_memory"):
       return self._memory
       
      import tracemalloc
      self._memory = tracemalloc
      return self.__enable_feature_memory(features=features, **kwargs )

  def memory_performance(self, raise_exception_not_init = True, **kwargs):
    if hasattr(self, "_memory"):
      return self._memory
    
    if raise_exception_not_init:
      raise self._main_reference.exception().exception(
        exception_type = "generic"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        message = f"Memory tracing not defined"
      )
    return None

  def startstop_tracemalloc(self, action = None, *args, **kwargs):
    memory_performance = self.memory_performance(raise_exception_not_init= False)
    if memory_performance is None:
      raise self._main_reference.exception().exception(
        exception_type = "generic"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        message = f"Memory tracing not defined"
      )
    if action is None:
      if memory_performance.is_tracing():
        return memory_performance.stop()
      return memory_performance.start()
    
    if action.lower() == "start":
      return memory_performance.start()
    
    return memory_performance.stop()
  
  def start_performance_monitoring(self, *args, **kwargs):    
    self.startstop_tracemalloc(action= "start")
      
  
  def stop_performance_monitoring(self, *args, **kwargs):
    self.startstop_tracemalloc(action= "stop")
  
  def performance_monitoring_memory_snapshot(self, clear_tracing = False):    
    memory_performance = self.memory_performance(raise_exception_not_init= False)
    if memory_performance is None:
      raise self._main_reference.exception().exception(
        exception_type = "generic"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        message = f"Memory tracing not defined"
      )

    snapshot = memory_performance.take_snapshot()
    if clear_tracing:
      memory_performance.clear_traces()
    return snapshot
  
  def performance_monitoring_memory(self, *args, **kwargs):
    memory_performance = self.memory_performance(raise_exception_not_init= False)
    if memory_performance is None:
      raise self._main_reference.exception().exception(
        exception_type = "generic"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        message = f"Memory tracing not defined"
      )

    return {
      "traced_memory": memory_performance.get_traced_memory(),
      "tracemalloc_memory": memory_performance.get_tracemalloc_memory()
    }