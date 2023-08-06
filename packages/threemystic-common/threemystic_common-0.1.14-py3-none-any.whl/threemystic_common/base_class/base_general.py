from threemystic_common.base_class.base import base as main_base

class base(main_base): 
  """This is a set of library wrappers to help general python apps"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    self._init_main(*args, **kwargs )
    self._init_common(*args, **kwargs)
    self._logger_init(*args, **kwargs)

    self._custom_init_post_base_init()
  
  def _custom_init_post_base_init(self, *args, **kwargs):
    pass   
  
  


  
    
