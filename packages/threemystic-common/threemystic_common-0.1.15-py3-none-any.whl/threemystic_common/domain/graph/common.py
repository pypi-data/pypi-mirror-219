from threemystic_common.base_class.base_common import base


class graph_common(base): 
  """This is a common set of methods and libraries"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"graph", *args, **kwargs)
  
  def __get_supported_graphs(self):
    return ["msgraph"]
  
  def init_graph(self, graph_method, *args, **kwargs):    
    graph_method = graph_method.lower() if graph_method is not None else ""
    
    if graph_method not in self.__get_supported_graphs():
      raise self._main_reference.exception().exception(
        exception_type = "generic"
      ).not_implemented(
        logger = self._main_reference.get_common().get_logger(),
        name = "graph_method",
        message = f"Unknown Graph Provided: {graph_method}.\nSupported Graph Providers{self.__get_supported_graphs()}"
      )

    if not hasattr(self, "_graph_method"):
      self._graph_method = {}
    
    if graph_method == "msgraph":
      from threemystic_common.domain.graph.msgraph import graph_msgraph as graph
      self._graph_method[graph_method] = graph(
        main_reference= self._main_reference,
        *args, **kwargs
      )

  def graph(self, graph_method, unset = False, *args, **kwargs):
    if(unset):
      if graph_method is None:
        self._unset("_graph_method")
        return
      if hasattr(self, "_graph_method"):
        if self._graph_method.get(graph_method) is not None:
          self._graph_method.pop(graph_method)

      return    
    
    graph_method = graph_method.lower() if graph_method is not None else ""
    if hasattr(self, "_graph_method"):
      if self._graph_method.get(graph_method) is not None:
        return self._graph_method[graph_method]
   
    self.init_graph(graph_method= graph_method, *args, **kwargs)
    return self.graph(graph_method= graph_method, *args, **kwargs)

