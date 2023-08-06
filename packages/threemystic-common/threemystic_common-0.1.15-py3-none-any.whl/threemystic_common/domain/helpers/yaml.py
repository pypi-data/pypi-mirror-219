import ruamel.yaml as yaml

from threemystic_common.base_class.base_common import base


class helper_yaml(base): 
  """This is a set of library wrappers to help around expending json libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_json", *args, **kwargs)

  def dumps(self, data, multiple_documents = False, use_safe = True, *args, **kwargs):   
    if not multiple_documents:
      return yaml.safe_dump(data, default_flow_style= False) if use_safe else yaml.dump(data)

    return yaml.safe_dump_all(data, default_flow_style= False) if use_safe else yaml.dump_all(data)
  
  def loads(self, data, return_empty_on_null = True, multiple_documents = False, use_safe = True,  *args, **kwargs):   
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
    from io import StringIO
    yaml_stream = StringIO(data)
    return self._load_stream(yaml_stream= yaml_stream, multiple_documents= multiple_documents, use_safe= use_safe)

  def load_file(self, path, multiple_documents = False, use_safe = True,  *args, **kwargs):
    with self._main_reference.helper_path().get(path= path).open(mode= 'r') as yaml_stream:
      return self._load_stream(yaml_stream= yaml_stream, multiple_documents= multiple_documents, use_safe= use_safe)

  def _load_stream(self, yaml_stream, multiple_documents, use_safe, *args, **kwargs):    
    if not multiple_documents:
      return yaml.safe_load(stream= yaml_stream) if use_safe else yaml.load(stream= yaml_stream, Loader=yaml.FullLoader)  

    docs = yaml.safe_load_all(stream= yaml_stream) if use_safe else yaml.load_all(stream= yaml_stream, Loader=yaml.FullLoader)  
    return [doc for doc in docs]