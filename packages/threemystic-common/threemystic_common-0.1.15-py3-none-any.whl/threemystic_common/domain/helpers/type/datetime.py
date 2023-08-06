from datetime import datetime, timedelta

from dateutil import tz as dateutil_tz
from threemystic_common.base_class.base_common import base
from zoneinfo import ZoneInfo
import math



class helper_type_datetime(base): 
  """This is a set of library wrappers to help around expending datetime libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_type_datetime", *args, **kwargs)
  
  # get_utc_datetime
  # get_utc
  def get(self, time_zone = "utc", *args, **kwargs):    
    utc = self.convert_to_utc(dt=datetime.utcnow(), default_utctime= True)
    return self.convert_time_zone(dt= utc, time_zone= time_zone)
  
  def time_delta(self, microseconds = 0, milliseconds= 0, seconds = 0, minutes =0, hours = 0, days = 0, weeks = 0, months = 0, years = 0, dt = None,  *args, **kwargs):
    """
    dt argument is only needed when using months or years. If None it uses utc_now
    """
    return_data = timedelta(
      microseconds= microseconds,milliseconds= milliseconds,
      seconds= seconds, minutes= minutes, hours= hours,
      days= days, weeks= weeks )
    
    years = self._main_reference.helper_type().int().get(int_value= years, default= 0)
    months = self._main_reference.helper_type().int().get(int_value= months, default= 0)
    
    if dt is None:
      dt = self.get()

    current_month = dt.month
    while (months + current_month) <= 0 or (months + current_month) > 12:
      months = (months + current_month)
      if months <= 0:
        years -= 1
        current_month = 12
        continue

      if months > 12:
        months -= 12
        years += 1
        current_month = 0
        continue
      
      
    current_month += months
    
    month_year_dt = self.parse_iso(
      iso_datetime_str= f'{dt.year + years}-{self.get_month_as_2digits(month= current_month)}-01{self.datetime_as_string(dt_format="T%H:%M:%S.%f", dt= dt)}+00:00'
    )
    
    dt_day = dt.day
    last_day_of_month = self.last_day_month_day(month= month_year_dt.month, year= month_year_dt.year)
    if dt_day > last_day_of_month:
      dt_day = 1
      current_month += 1
      if current_month > 12:
        current_month = 1
        years += 1
    # YYYY-MM-DDTHH:MM:SS.mmmmmm    
    year_month_parsed_dt = (self.parse_iso(
      iso_datetime_str= f'{dt.year + years}-{self.get_month_as_2digits(month= current_month)}-{self.get_day_as_2digits(day= dt_day)}{self.datetime_as_string(dt_format="T%H:%M:%S.%f", dt= dt)}+00:00'
    ) + return_data)
    
    return_data = (year_month_parsed_dt - dt)
    return return_data
  
  def time_delta_seconds(self, total_seconds = 300, time_zone="utc", *args, **kwargs):    
    return self.time_delta(
      total_seconds= total_seconds,
      time_zone= time_zone,
      *args, **kwargs
    )
  
  def get_epoch(self, *args, **kwargs):    
    return self.convert_to_utc(dt= datetime.utcfromtimestamp(0))
  
  def get_timestamp(self, dt, *args, **kwargs):
    return dt.timestamp()
  
  def get_from_timestamp(self, time_delta, *args, **kwargs):
    if self._main_reference.helper_type().general().is_type(time_delta, int):
      time_delta = timedelta(milliseconds= time_delta)

    return (self.convert_to_utc(dt= datetime.utcfromtimestamp(0)) + time_delta)

  # convert_datetime_utc
  def convert_to_utc(self, dt, default_utctime = True, *args, **kwargs):   
    if dt.tzinfo is None:
      dt = (dt.replace(tzinfo=dateutil_tz.tzutc() if default_utctime else dateutil_tz.tzlocal()))
          
    return dt.astimezone(dateutil_tz.tzutc())
  
  def datetime_as_string(self, dt_format = "%Y%m%d%H%M%S", dt = None, time_zone="utc", *args, **kwargs):    
    if dt is None:
      dt = self.get(time_zone= time_zone)
    
    return dt.strftime(dt_format)
  
  # get_tzinfo_from_datetime
  def get_tzinfo(self, check_datetime, default_tz, *args, **kwargs):
    
    if check_datetime.tzinfo is not None:
      return check_datetime.tzinfo
    
    return self.get_time_zone(time_zone= default_tz)

  # get_tzinfo
  def get_time_zone(self, time_zone, default_utc = True, *args, **kwargs):
    if not self._main_reference.helper_type().general().is_type(time_zone, str):
      return dateutil_tz.tzutc() if default_utc else dateutil_tz.tzlocal()
      
    if not self._main_reference.helper_type().string().is_null_or_whitespace(time_zone):
      return dateutil_tz.tzutc() if default_utc else dateutil_tz.tzlocal()

    if time_zone.lower() == "utc":
      return dateutil_tz.tzutc()
    
    if time_zone.lower() == "local":
      return dateutil_tz.tzlocal()

    return ZoneInfo(time_zone)
  
  def get_offset_from_zoneinfo(self, zoneinfo, return_as_timedelta = False, *args, **kwargs):   
    if not return_as_timedelta:
      return datetime.now(tz= zoneinfo).strftime('%z')
    
    return datetime.now(tz= zoneinfo).utcoffset()
  
  def convert_time_24hours(self, time_str, error_missing_ampm= False, *args, **kwargs):   
    is_am = False
    if time_str[-2].lower() == "am" or time_str[-1].lower() == "a":
      is_am = True
    
    if not is_am and time_str[-2].lower() != "pm" and time_str[-1].lower() != "p":
      if error_missing_ampm:
        raise self._main_reference.exception().exception(
        exception_type = "generic"
        ).type_error(
          logger = self._main_reference.get_common().get_logger(),
          message = f"missing am/pm indicator"
        )
      return time_str
    
    time_parts = self._main_reference.helper_type().string().split(string_value=time_str.rstrip(" amp"), separator=":")
    for idx,part in enumerate(time_parts):
      time_parts[idx]=int(part)
    
    if not is_am:
      time_parts[0] += 12

    for idx,part in enumerate(time_parts):
      time_parts[idx]=str(part) if part>9 else f"0{part}"
    
    if len(time_parts) <3:
      time_parts.append("00")
    
    return ":".join(time_parts)
      
  # get_datetime_nearest_minute
  def get_nearest_minute(self, dt = None, minute = 15, time_zone= "utc", *args, **kwargs):    
    if dt is None:
      dt = self.get(time_zone= time_zone)

    return datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour,minute=minute*int(math.floor((dt.minute / minute))), tzinfo= dt.tzinfo)

  # get_datetime_nearest_next_minute
  def get_nearest_next_minute(self, dt = None, minute = 15, time_zone= "utc", *args, **kwargs):  
    if dt is None:
      dt = self.get(time_zone= time_zone)

    next_nearest_minute = minute*(int(math.floor((dt.minute / minute)))+ 1)
    if next_nearest_minute < 60:
      return datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour,minute=next_nearest_minute, tzinfo= dt.tzinfo)
    
    return dt + self.time_delta(seconds=((next_nearest_minute - dt.minute) * 60))

  def datetime_from_string(self, dt_string, dt_format="%Y/%m/%d", *args, **kwargs):    
    if self._main_reference.helper_type().general().is_type(dt_format, str):
      try:
        return self.convert_to_utc(dt= datetime.strptime(dt_string, dt_format ))
      except:
        return None
    
    if self._main_reference.helper_type().general().is_type(dt_format, list):
      for format in dt_format:
        try:
          format_value = self.datetime_from_string(dt_string= dt_string, dt_format=format)
          if format_value is not None:
            return format_value
        except:
          continue

    return None
    

  # parse_datetime_iso
  def parse_iso(self, iso_datetime_str, *args, **kwargs):    
    if self._main_reference.helper_type().string().set_case(string_value= iso_datetime_str, case= "lower")[-1] == "z":
      iso_datetime_str = f"{iso_datetime_str[0:len(iso_datetime_str) - 1]}+00:00"
    
    return datetime.fromisoformat(iso_datetime_str)
  
  def get_iso_datetime(self, dt = None, *args, **kwargs):    
    if dt is None:
      dt = self.get()
    
    iso_format = dt.isoformat(sep="T",timespec='auto')
    if iso_format.endswith("00:00"):
      iso_format = iso_format[0:len(iso_format)-5]
      if iso_format.endswith("+") or iso_format.endswith("+"):
        iso_format = iso_format[0:len(iso_format)-1]
      iso_format = f'{iso_format}Z'
    
    return iso_format
  

  # convert_datetime_utc
  def convert_utc(self, dt, default_utctime = True):   
    if dt.tzinfo is None:
      dt = (dt.replace(tzinfo=dateutil_tz.tzutc() if default_utctime else dateutil_tz.tzlocal()))
          
    return self.convert_time_zone(
      dt= dt,
      time_zone = "utc"
    )
  
  def set_tzinfo(self, dt, time_zone = "utc", force_replace = False, *args, **kwargs):    
    
    if dt.tzinfo is not None and not force_replace:
      dt = dt.astimezone(self.get_time_zone(time_zone))
      return dt

    dt =  dt.replace(tzinfo=self.get_time_zone(time_zone))
    return dt


  # convert_datetime
  def convert_time_zone(self, dt = None, time_zone = "utc", base_time_zone = "utc", *args, **kwargs):    
    if dt is None:
      dt = self.get(time_zone= time_zone)
    
    dt_time_zone = self.get_tzinfo(check_datetime= dt, default_tz= base_time_zone)
    self.set_tzinfo(dt= dt, time_zone=dt_time_zone, force_replace= True)
    time_zone = self.get_time_zone(time_zone= time_zone)
    return dt.astimezone(time_zone) 

  # remove_tzinfo_datetime
  def remove_tzinfo(self, dt, default_utctime = True, *args, **kwargs):         
    return self.convert_to_utc(dt= dt, default_utctime= default_utctime).replace(tzinfo=None)

  # convert_datetime_local
  def convert_local(self, dt, time_zone= "utc", *args, **kwargs):
    if dt is None:
      dt = self.get(time_zone= time_zone)
    
    dt_time_zone = self.get_tzinfo(check_datetime= dt, default_tz= None)
    self.set_tzinfo(dt= dt, time_zone=dt_time_zone, force_replace= True)
    return self.convert_time_zone(
      dt= dt,
      time_zone = "local"
    )
  
  # datetime_ticks_as_seconds
  def ticks_as_seconds(self, dt, tick_startdate = datetime(year= 1, month= 1, day= 1, hour= 0, minute= 0, tzinfo= dateutil_tz.tzutc()), *args, **kwargs):
    dt = self.convert_to_utc(dt)
    if tick_startdate is None:
      tick_startdate = datetime(year= 1, month= 1, day= 1, hour= 0, minute= 0, tzinfo= dateutil_tz.tzutc())

    tick_startdate = self.convert_to_utc(tick_startdate)
    return (dt - tick_startdate).total_seconds()

  # datetime_ticks
  def ticks(self, dt, tick_startdate = datetime(year= 1, month= 1, day= 1, hour= 0, minute= 0, tzinfo= dateutil_tz.tzutc()), *args, **kwargs):
    return self.ticks_as_seconds(dt= dt, tick_startdate= tick_startdate) * 10**7
  
  # isTokenExpired_Now
  def is_token_expired_now(self, compare_datetime, buffer_delta = timedelta(seconds=300)):   
    return (self.convert_utc(compare_datetime) <= (self.convert_utc(self.get(time_zone= "local")) - buffer_delta))

  # isTokenExpired_Duration
  def is_token_expired(self, token_life_duration, start_time = None, buffer_delta = timedelta(seconds=60), time_zone= "utc", *args, **kwargs):  
    if start_time is None:
      start_time = self.get(time_zone= time_zone)
    return (start_time + token_life_duration) <= (self.get(time_zone= time_zone - buffer_delta))
  
  # isTokenExpiredEpoch_Duration
  def is_token_expired_epoch(self, token_life_duration, start_time = None, buffer_delta = timedelta(seconds=300), time_zone= "utc", *args, **kwargs):  
    if start_time is None:
      start_time = self.get_epoch()
    return self.token_expired_epoch(token_life_duration= token_life_duration, start_time= start_time) <= (self.get(time_zone= time_zone) - buffer_delta)
  
  # GetTokenExpiredEpoch_Duration
  def token_expired_epoch(self, token_life_duration, start_time = None, *args, **kwargs):  
    if start_time is None:
      start_time = self.get_epoch()
    return (start_time + token_life_duration)
  
  def get_month_as_2digits(self, month, *args, **kwargs):  
    if int(month) < 10:
      return f'0{month}'
    
    return month

  def get_day_as_2digits(self, day, *args, **kwargs):  
    if int(day) < 10:
      return f'0{day}'
    
    return day
  
  def yesterday(self, dt = None, *args, **kwargs):  
    if dt is None:
      dt = self.get(*args, **kwargs)
    return (dt - timedelta(days= 1))
  
  def last_day_month(self, month, year = None, *args, **kwargs):  
    if year is None:
      year = self.get().year

    month = int(month) + 1
    if month > 12:
      month = 1
      year = (year) + 1

    dt = self.datetime_from_string(f"{year}/{self.get_month_as_2digits(month= month)}/01")
    return (dt - timedelta(days= 1))
  
  def last_day_month_day(self, month, year = None, *args, **kwargs):      
    return self.last_day_month(month= month, year= year).day