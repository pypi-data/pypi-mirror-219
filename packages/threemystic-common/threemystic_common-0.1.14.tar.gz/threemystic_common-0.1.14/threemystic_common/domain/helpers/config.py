from pathlib import Path
from threemystic_common.base_class.base_common import base
import configparser

class helper_config(base): 
  """This is a set of library wrappers to help general python apps"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_config", *args, **kwargs)

  def _get_known_config_types(self, *args, **kwargs):
    return ["json", "config", "yaml"]

  # load_defaults_config
  def load(self, config_type = "yaml", *args, **kwargs):
    if self._main_reference.helper_type().string().is_null_or_whitespace(config_type):
      raise self._main_reference.exception().exception(
        exception_type = "argument"
      ).type_error(
        logger = self._main_reference.get_common().get_logger(),
        name = "config_type",
        message = f"config_type is either None or an empty string"
      )
    
    if config_type.lower() not in self._get_known_config_types():
      raise self._main_reference.exception().exception(
        exception_type = "generic"
      ).not_implemented(
        logger = self._main_reference.get_common().get_logger(),
        name = "config_type",
        message = f"config_type not known, known values: {self._get_known_config_types()}"
      )
    
    if config_type.lower() == "config":
      return self._load_defaults_config_config(config_type= config_type, *args, **kwargs)
    

    return self._load_defaults_config_general(config_type= config_type, *args, **kwargs)
    
  def _load_path(self, path, config_key = None, config_name = None, *args, **kwargs):
    if self._main_reference.helper_type().string().is_null_or_whitespace(path):
      return None
    
    path = self._main_reference.helper_path().get(path=path )
    if not self._main_reference.helper_type().string().is_null_or_whitespace(config_key):
      return path.joinpath(config_key)
    if not self._main_reference.helper_type().string().is_null_or_whitespace(config_name):
      return path.joinpath(config_name)
    
    if not self._main_reference.helper_path().is_file(path=path):
      return None
      
    return path

  def _load_defaults_config_config(self, path, *args, **kwargs):
    config_parser = configparser.ConfigParser()
    if self._main_reference.helper_type().string().is_null_or_whitespace(path):
      return config_parser
    
    config_path = self._main_reference.helper_path().get(path=path )
    if not config_path.exists():
      return config_parser

    with config_path.open("r") as config_stream:
      config_parser.read_file(config_stream)
    
    return config_parser
  
  def _get_load_data_function(self, config_type):
    return self._load_defaults_config_json_data if config_type == "json" else self._load_defaults_config_yaml_data

  def _load_defaults_config_general(self, config_type, path, config_key = None, config_name = None, replace_on_merge = False, path_override = None,  return_as_config = False, *args, **kwargs):
    load_data_function = self._get_load_data_function(config_type= config_type)
    defaults_config = load_data_function(
      path = path, 
      config_key = config_key, 
      config_name = config_name
    )

    if self._main_reference.helper_type().string().is_null_or_whitespace(path_override):
      path_override = f"{path}/override"
    
    override_config = load_data_function(
      path = path_override, 
      config_key = config_key, 
      config_name = config_name
    )
    
    if not return_as_config:
      return self._main_reference.helper_type().dictionary().merge_dictionary([ {}, defaults_config, override_config], replace_on_merge= replace_on_merge)
    
    config_parser = configparser.ConfigParser()
    return config_parser.read_dict(self._main_reference.helper_type().dictionary().merge_dictionary([ {}, defaults_config, override_config], replace_on_merge= replace_on_merge))
  
  def _load_defaults_config_json_data(self, path, config_key, config_name, *args, **kwargs):
    if self._main_reference.helper_type().string().is_null_or_whitespace(path):
      return {}

    config_path = self._load_path(path= path, config_key= config_key, config_name= config_name)
    if config_path is None:
      return {}

    return self._main_reference.helper_json().load_file(
      path= config_path,
      return_empty_on_null= True
    )
  
  
  def _load_defaults_config_yaml_data(self, path, config_key, config_name, *args, **kwargs):
    if self._main_reference.helper_type().string().is_null_or_whitespace(path):
      return {}
    
    config_path = self._load_path(path= path, config_key= config_key, config_name= config_name)
    if config_path is None:
      return {}

    return self._main_reference.helper_yaml().load_file(path= config_path)