import json
from datetime import datetime
from zoneinfo import ZoneInfo

import dateutil.tz as dateutil_tz
import decimal
from threemystic_common.base_class.base_common import base


class helper_json(base): 
  """This is a set of library wrappers to help around expending json libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_json", *args, **kwargs)
  
  def __get_offset_from_zoneinfo(cls, zoneinfo, return_as_timedelta = False):   
    if not return_as_timedelta:
      return datetime.now(tz= zoneinfo).strftime('%z')
    
    return datetime.now(tz= zoneinfo).utcoffset()

  # json_dumps_serializable_default
  def serializable_default(self, data, *args, **kwargs):
    if self._main_reference.helper_type().general().is_type(data, datetime) or self._main_reference.helper_type().general().is_type(data, type(datetime.now().time())):
      return data.isoformat()

    if self._main_reference.helper_type().general().is_type(data, [ dateutil_tz.tz.tzutc,  dateutil_tz.tz.tzlocal, ZoneInfo]):
      return self.__get_offset_from_zoneinfo(data)
    
    if self._main_reference.helper_type().general().is_type(data, decimal.Decimal):
      return str(data)
    try:
      json.dumps(data)
    except:
      if hasattr(data, "__dict__"):
        return data.__dict__
      raise

    return data

  def dumps(self, data, default_encoder_function = None, *args, **kwargs):   
    if kwargs.get("default") is None:
      kwargs["default"] = self.serializable_default if default_encoder_function is None else default_encoder_function
    return json.dumps(data, **kwargs)
  
  def loads(self, data, return_empty_on_null = True,  *args, **kwargs):   
    if data is None:
      return {} if return_empty_on_null else None

    if not self._main_reference.helper_type().general().is_type(data, str):
      raise self._main_reference.exception().exception(
        exception_type = "argument"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        name = "data",
        message = f"attribute is not of type string - {type(data)}"
      )

    return json.loads(data)

  def load_file(self, path, return_empty_on_null = True, *args, **kwargs):
    with self._main_reference.helper_path().get(path= path).open(mode= 'r') as json_stream:
      json_data = json_stream.read()

    return self.loads(
      data= json_data,
      return_empty_on_null= return_empty_on_null
    )  