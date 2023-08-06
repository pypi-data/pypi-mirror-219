from threemystic_common.base_class.base_common import base


class helper_type_string(base): 
  """This is a set of library wrappers to help around expending string libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_type_string", *args, **kwargs)
  
  def join(self, separator, str_array, return_empty_if_null = True, *args, **kwargs):
    if not return_empty_if_null and str_array is None:
      return None
    if return_empty_if_null and str_array is None:
      return ""

    if self.is_null_or_whitespace(string_value= separator):
      separator = ""
      
    if self._main_reference.helper_type().general().is_type(str_array, list):
      str_array = [item for item in str_array if item is not None]
      if(len(str_array) < 1):
        return ""
      if(len(str_array) == 1):
        return str_array[0]

      return separator.join(str_array)
    
    raise self._main_reference.exception().exception(
        exception_type = "argument"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        name = "str_array",
        message = f"str_array is not a list"
      )
  
  def ltrim(self, string_value, trim_chars = None, return_empty_if_null = True, *args, **kwargs):
    if not return_empty_if_null and string_value is None:
      return None

    if self.is_null_or_whitespace(string_value= string_value):
      return ""
    
    return string_value.lstrip() if trim_chars is None else string_value.lstrip(trim_chars)
  
  def rtrim(self, string_value, trim_chars = None, return_empty_if_null = True, *args, **kwargs):
    if not return_empty_if_null and string_value is None:
      return None

    if self.is_null_or_whitespace(string_value= string_value):
      return ""
    
    return string_value.rstrip() if trim_chars is None else string_value.rstrip(trim_chars)
  
  def trim(self, string_value, trim_chars = None, return_empty_if_null = True, *args, **kwargs):
    if not return_empty_if_null and string_value is None:
      return None

    if self.is_null_or_whitespace(string_value= string_value):
      return ""
    
    if not self._main_reference.helper_type().general().is_type(obj= string_value, type_check= str):
      string_value = str(string_value)

    return string_value.strip() if trim_chars is None else string_value.strip(trim_chars)


  def set_case(self, string_value, case = "upper", *args, **kwargs):
    if self.is_null_or_whitespace(string_value= string_value):
      return string_value
    
    if not self._main_reference.helper_type().general().is_type(obj= string_value, type_check= str):
      return string_value
    
    case = self.trim(string_value=case).lower()
    
    
    if case == "upper":
      return string_value.upper()
    
    if case == "lower":
      return string_value.lower()
    
    if case == "camel":
      caseWords = self.split(string_value= string_value, separator=r"\s")
      if len(caseWords) < 1:
        return ""
      
      camelStr= "".join([word[0].upper() + word[1:].lower() for word in caseWords])
      return camelStr[0].lower() + camelStr[1:]
    
    if case == "pascal":
      caseWords = self.split(string_value= string_value, separator=r"\s")
      if len(caseWords) < 1:
        return ""
      
      return "".join([word[0].upper() + word[1:].lower() for word in caseWords])
    
    if case == "snake":
      caseWords = self.split(string_value= string_value, separator=r"\s")
      if len(caseWords) < 1:
        return ""
      
      return "_".join([word[0].lower() + word[1:].lower() for word in caseWords])
    
    valid_case_options = ["upper", "lower", "camel", "pascal", "snake"]
    raise self._main_reference.exception().exception(
        exception_type = "argument"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        name = "case",
        message = f"case type is unknown. valid options: {valid_case_options}"
      )
  
  # isNullOrWhiteSpace
  def is_null_or_whitespace(self, string_value, *args, **kwargs):
    
    if not string_value:
      return True

    if str(string_value).strip() == "":
      return True
    
    return False
  
  # split_string
  def split(self, string_value, trim_data = True, remove_empty = True, separator = "[,;]", regex_split = True, *args, **kwargs):
    
    if regex_split:
      return self._main_reference.helper_type().regex().split(
        string_value= string_value,
        trim_data= trim_data,
        remove_empty= remove_empty,
        separator= separator
      )
    
    split_data = string_value.split(separator)
    
    if not remove_empty:
      return split_data if not trim_data else [str(item).strip() if item is not None else item for item in split_data ]
      
    if not trim_data:
      return [item for item in split_data if not self.is_null_or_whitespace(item)]

    return [item.strip() for item in split_data if not self.is_null_or_whitespace(item)]