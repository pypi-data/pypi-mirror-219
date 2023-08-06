
from threemystic_common.base_class.base_common import base


class helper_app(base): 
  """This is a set of library wrappers to help general python apps"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_app", *args, **kwargs)
  
  def __is_type(cls, obj, type_check, *args, **kwargs):
    try:
      return isinstance(obj, type_check)
    except:
      return type(obj) == type_check
  
  def get_output_levels(self):
    return {
    "verbose": 1000,
    "debug": 500,
    "information": 100,
    "quiet": 20,
    "main": 10,
    "suppress": 0
    }
  
  def get_output_level(self, output_dictionary, *args, **kwargs):
    output_output_level = output_dictionary.get("output_output_level") if output_dictionary.get("output_output_level") is not None else -1
    if output_output_level > -1:
      return output_output_level

    output_verbose = output_dictionary.get("output_verbose") if output_dictionary.get("output_verbose") is not None else False
    if output_verbose:
      return self.get_output_levels()["verbose"]
    
    output_quiet = output_dictionary.get("output_quiet") if output_dictionary.get("output_quiet") is not None else False
    if output_quiet:
      return self.get_output_levels()["quiet"]
    
    output_suppress = output_dictionary.get("output_suppress") if output_dictionary.get("output_suppress") is not None else False
    if output_suppress:
      return self.get_output_levels()["suppress"]
    
    return self.get_output_levels()["information"]
  
  def show_output(self, output_level, output_dictionary, *args, **kwargs):
    output_levels = self.get_output_levels()  
  
  
    output_level_int = output_levels.get(output_level) if output_levels.get(output_level) is not None else output_levels.get("verbose")
    if output_level_int > self.get_output_level(output_dictionary):
      return False

    return True
  
  def outputlevel_ok(self, output_level, max_acceptable_level, *args, **kwargs):
    output_levels = self.get_output_levels()  
    if self.__is_type(output_level, str):
      output_level = output_levels.get(output_level) if output_levels.get(output_level) is not None else output_levels.get("main")
  
    if self.__is_type(max_acceptable_level, str):
      max_acceptable_level = output_levels.get(max_acceptable_level)

    
    return True if output_level <= max_acceptable_level else False

  def start_processing_time(self, dateStart = None, *args, **kwargs):
    if dateStart is None:
      dateStart = self._main_reference.helper_type().datetime().get_utc_datetime()
    return dateStart