from threemystic_common.base_class.base_common import base


class generate_data(base): 
  
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"generate_data", *args, **kwargs)
  
  def _get_restricted_keynames(self, *args, **kwargs):
    if hasattr(self, "_restricted_keynames"):
      return self._restricted_keynames

    self._restricted_keynames = ["meta_data"]
    return self._get_restricted_keynames(*args, **kwargs)

  def generate(self, generate_data_config, *args, **kwargs):
    return self._generate(generate_data_config= generate_data_config, *args, **kwargs)

  def _generate(self, generate_data_config, is_child_elemement = False, *args, **kwargs):
    
    return_data = {}
    
    for key, item in generate_data_config.items():
      if key.lower() in self._get_restricted_keynames() and not is_child_elemement:
        raise self._main_reference.exception().exception(
          exception_type = "argument"
        ).exception(
          logger = self._main_reference.get_common().get_logger(),
          name = "generate_data_config",
          message = f"Contains an element using a reserved key: {key}. Reserved Keys: {self._get_restricted_keynames()}"
        )   

      if item.get("skip") is not None:
        if item["skip"](return_data):
          return_data[key] = None
          continue

      if item.get("handler") is None:
        raise self._main_reference.exception().exception(
            exception_type = "argument"
          ).type_error(
            logger = self._main_reference.get_common().get_logger(),
            name = "generate_data_config",
            message = f"Handler cannot be None for key: {key}."
          )
        
      if item.get("children") is not None:
        item.get("handler").print_descrinption(item)

        if self._main_reference.helper_type().general().is_type(item["children"], dict):
          return_data[key] = self._generate(generate_data_config= item, *args, **kwargs)
          continue
        
        if self._main_reference.helper_type().general().is_type(item["children"], list):
          return_data[key] = [
            self._generate(generate_data_config= child, *args, **kwargs) for child in self._generate(generate_data_config= item, return_data= return_data, *args, **kwargs)
          ]
            
          continue
        
        if key.lower() in self._get_restricted_keynames() and not is_child_elemement:
          raise self._main_reference.exception().exception(
            exception_type = "argument"
          ).type_error(
            logger = self._main_reference.get_common().get_logger(),
            name = "generate_data_config",
            message = f"Unknown children type. Should be either a Dictrionary of children or a list. Got Type {type(item['children'])}"
          )
        continue
      
      return_data[key] = item.get("handler").generate(
        attribute_name= key, 
        item= item
      )
      
      if return_data[key] is None or return_data[key].get("quit") == True:
        print("Exiting now. No Data Saved")
        return None

      if "raw" not in return_data[key] is None or "formated" not in return_data[key] is None:
        raise self._main_reference.exception().exception(
            exception_type = "function"
          ).exception(
            logger = self._main_reference.get_common().get_logger(),
            name = "handler",
            message = f"Handler for Key: {key} did not return proper response. Should return a dictionary with raw and formated"
          )
    
    return return_data
      
      

