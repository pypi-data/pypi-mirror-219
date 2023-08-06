from pathlib import Path  
from pathvalidate import sanitize_filepath, sanitize_filename
from threemystic_common.base_class.base_common import base

class helper_path(base): 
  """This is a set of library wrappers to help around expending json libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_path", *args, **kwargs)
  
  def is_valid_filepath(self, path, *args, **kwargs):
    return sanitize_filepath(path) == path
  
  def is_valid_filename(self, file_name, *args, **kwargs):
    return sanitize_filename(file_name) == file_name

  # report_directory
  def get(self, path = None, *args, **kwargs)->Path:
    if path is None:
      return None
    if self._main_reference.helper_type().general().is_type(path, Path):
      return path

    if not self._main_reference.helper_type().general().is_type(path, str):
      raise self._main_reference.exception().exception(
        exception_type = "argument"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        name = "path",
        message = f"Unknown type ({type(path)})"
      )
    
    if self._main_reference.helper_type().string().is_null_or_whitespace(path):
      raise self._main_reference.exception().exception(
        exception_type = "argument"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        name = "path",
        message = f"path is either None or an empty string"
      )
    
    return Path(path)
  
  def expandpath_user(self, path) -> Path:
    if self._main_reference.helper_type().general().is_type(path, Path):
      return path.expanduser()
    
    return self.get(path).expanduser()
  
  def path_exists(self, path):
    if self._main_reference.helper_type().general().is_type(path, Path):
      return path.exists()

    if not self._main_reference.helper_type().general().is_type(path, str):
      raise self._main_reference.exception().exception(
        exception_type = "argument"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        name = "path",
        message = f"path is not a string or Path type"
      )  
    
    if self._main_reference.helper_type().string().is_null_or_whitespace(path):
      raise self._main_reference.exception().exception(
        exception_type = "argument"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        name = "path",
        message = f"path is either None or an empty string"
      )

    path = self.get(path= path)
    if path is None: 
      return False

    return path.exists()

  def is_file(self, path):
    path = self.get(path= path)
    if path is None: 
      return False

    if not path.exists(): 
      return False

    return Path.is_file(self.get(path= path))
  
  def is_dir(self, path):
    path = self.get(path= path)
    if path is None: 
      return False

    if not path.exists(): 
      return False

    return Path.is_dir(self.get(path= path))
  
  
    
