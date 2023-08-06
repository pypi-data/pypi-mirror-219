from openpyxl.utils import get_column_letter
from threemystic_common.base_class.base_common import base



class helper_type_openpyxl(base): 
  """This is a set of library wrappers to help around expending list libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_type_openpyxl", *args, **kwargs)
  
  def convert_column_index_to_letter(self, column_index):
    '''Zero based column index'''

    return get_column_letter(column_index)