from threemystic_common.base_class.base_common import base
import re


class helper_type_regex(base): 
  """This is a set of library wrappers to help around expending string libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_type_string", *args, **kwargs)
  
  def get(self, pattern, flags=re.IGNORECASE) -> re.Pattern:
    return re.compile(pattern= pattern, flags= flags)

  def valid_email(self, check_str):
    if self._main_reference.helper_type().string().is_null_or_whitespace(check_str):
      return False
      
    email_validator = self.get(pattern=r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    return True if email_validator.fullmatch(string= check_str) else False
  
  def split(self, string_value, trim_data = True, remove_empty = True, separator = "[,;]"):
    split_data = re.split(separator, string_value)
    if not remove_empty:
      return split_data if not trim_data else [str(item).strip() if item is not None else item for item in split_data ]
      
    if not trim_data:
      return [item for item in split_data if not self._main_reference.helper_type().string().is_null_or_whitespace(item)]

    return [item.strip() for item in split_data if not self._main_reference.helper_type().string().is_null_or_whitespace(item)]