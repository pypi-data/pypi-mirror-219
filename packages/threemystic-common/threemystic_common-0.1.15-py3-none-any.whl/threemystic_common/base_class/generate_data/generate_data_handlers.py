

class generate_data_handlers:
  def __init__(self, *args, **kwargs):
    pass
  
  @classmethod
  def get_handler(cls, handler, *args, **kwargs):
    known_handlers = [
      "base"
    ]
    if str(handler).lower() not in known_handlers:
      return None
    
    if handler.lower() == "base":
      from threemystic_common.base_class.generate_data.handlers.base import base_handler as generate_handler
      return generate_handler()