from threemystic_common.domain.cmdb.base_class.base import cmdb_base as base


class cmdb_azure(base): 
  """This is a common set of methods and libraries"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= "cmdb_azure", *args, **kwargs)
  
  def get_source(self, *args, **kwargs):
    return "azure"
    
    
    
  