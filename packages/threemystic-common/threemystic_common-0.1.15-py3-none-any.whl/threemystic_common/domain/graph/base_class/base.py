from abc import abstractmethod
from threemystic_common.base_class.base_common import base
import requests,urllib

class graph_base(base): 
  """This is a set of library wrappers to help create a cmdb"""

  def __init__(self, credentials, graph_scope = None, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    
    if not self.__check_credentials(credentials= credentials, *args, **kwargs):
      raise self.get_common().exception().exception(
        exception_type = "argument"
      ).not_implemented(
        logger = self.get_common().get_logger(),
        name = "credentials",
        message = f"credentials requires a method caleld get_token to pull the token from, or a dict object with a key of get_token that is the method to pull the token from.\nFor python sdk support options please see: https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity?view=azure-python"
      )
    
    self.graph_scope = graph_scope
    self.__set_credentials(credentials= credentials, *args, **kwargs)

  @abstractmethod
  def create_folder_data(self, *args, **kwargs):
    pass

  @abstractmethod
  def generate_session_header(self, session_config, refresh= False,  refresh_session = False, *args, **kwargs):
    pass

  @abstractmethod
  def close_session(self, session_config, refresh = False, *args, **kwargs):
    pass

  @abstractmethod
  def create_file_data(self, *args, **kwargs):
    pass

  @abstractmethod
  def graph_scope_default(self, *args, **kwargs):
    pass

  @abstractmethod
  def openid_config_default(self, *args, **kwargs):
    pass

  @abstractmethod
  def generate_graph_url(self, *args, **kwargs):
    pass

  @abstractmethod
  def _get_auth_header(self, scope= None, refresh = False,  *args, **kwargs):
    pass
  
  @abstractmethod
  def generate_url_prefix(self, version = "v1.0", *args, **kwargs):
    pass

  @property
  def graph_credentials(self):
    return self.__graph_credentials
  
  @property
  def max_batch_size(self):
    if hasattr(self, "_max_batch_size"):
      return self._max_batch_size
    
    return 500

  @max_batch_size.setter
  def max_batch_size(self, value):
    self._max_batch_size = value
  # bring in the msgraph helper

  @property
  def graph_scope(self):
    if hasattr(self, "_graph_scope"):
      if self._graph_scope != None:
        if (self.get_common().helper_type().general().is_type(obj= self._graph_scope, type_check= str) and
            not self.get_common().helper_type().string().is_null_or_whitespace(string_value= self._graph_scope)):
          return self._graph_scope
    
    return self.graph_scope_default()

  @graph_scope.setter
  def graph_scope(self, value):
    if self.get_common().helper_type().string().is_null_or_whitespace(string_value= value):
      return
    
    if self.get_common().helper_type().general().is_type(obj= value, type_check= str):
      self._graph_scope = value
      return
    
    raise self.get_common().exception().exception(
      exception_type = "argument"
    ).type_error(
      logger = self.get_common().get_logger(),
      name = "value",
      message = f"value should either be a string, got: {type(value)}"
    )

  def __check_credentials(self, credentials, *args, **kwargs):
    if self.get_common().helper_type().general().is_type(obj= credentials, type_check= dict):
      if credentials.get("get_token") is None:
        return False
      return callable(credentials.get("get_token"))
    
    if not hasattr(credentials, "get_token"):
      return False
    
    return callable(credentials.get_token)
  
  def __set_credentials(self, credentials, *args, **kwargs):
    if not self.__check_credentials(credentials= credentials):
      return
    
    self.__graph_credentials = credentials

  def _process_params(self, params, *args, **kwargs):
    if params is None:
      return ""
    
    if (self.get_common().helper_type().general().is_type(obj= params, type_check= str) and 
        not self.get_common().helper_type().string().is_null_or_whitespace(string_value= params)):
      return f'?{params}'

    if self.get_common().helper_type().general().is_type(obj= params, type_check= dict):
      return f'?{urllib.parse.urlencode(params)}'
    
    raise self.get_common().exception().exception(
      exception_type = "argument"
    ).type_error(
      logger = self.get_common().get_logger(),
      name = "params",
      message = f"param is an known type: {type(params)} - valid options are string or dictionary"
    )
    
  def _get_request_method(self, method = "get", *args, **kwargs):
    if method.lower() == "post":
      return requests.post
    
    if method.lower() == "put":
      return requests.put

    if method.lower() == "delete":
      return requests.delete

    if method.lower() == "patch":
      return requests.patch
    
    return requests.get
  
  def get_openid_config(self, refresh = False, *args, **kwargs):
    if hasattr(self, "_base_openid_config") and not refresh:
      return self._base_openid_config

    req_session = requests.Session()
    result = req_session.get(self.openid_config_default(), 
      headers = { })

    if result.status_code != 200:
      raise self.get_common().exception().exception(
        exception_type = "generic"
      ).exception(
        logger = self.get_common().get_logger(),
        name = "HTTPREQUEST",
        message = f"openid_config: Non 200 status returned {result.status_code}"
      )      
    
    self._base_openid_config = result.json()
    return self.get_openid_config(*args, **kwargs)
  
  def send_request(self, url, method = "get", scope = None, params = None, headers = None, data = None, version = "v1.0", session_config = None, *args, **kwargs):    
    """
    This function is a general method to send requests. It will try to handel the call in a more graceful way
    """
    
    try:
      return self._send_request(
        url, method = method, scope = scope, 
        params = params, headers = headers, 
        data = data, version = version, 
        session_config = session_config, 
        *args, **kwargs
      )
    
    except requests.exceptions.HTTPError as err:
      if err.response.status_code == 401:
        self.get_common().get_logger().warning("MSGRAPH-Unauthorized for url")
        self._get_auth_header(scope= kwargs.get("graph_scope"), refresh= True)
        return self._send_request(
          url, method = method, scope = scope, 
          params = params, headers = headers, 
          data = data, version = version, 
          session_config = session_config, 
          *args, **kwargs
        )
      
      if err.response.status_code == 400:
        error_details = err.response.json()
        if self.get_common().helper_type().string().set_case(string_value= error_details.get("error").get("code"), case= "lower") == "invalidsession":
          if session_config is not None:
            self.generate_session_header(session_config= session_config, refresh= True, refresh_session= True )
            return self._send_request(
              url, method = method, scope = scope, 
              params = params, headers = headers, 
              data = data, version = version, 
              session_config = session_config, 
              *args, **kwargs
            )

      # need someway to track a bad refresh so it generates a new session.
      raise err
    except Exception as err:
      raise err
  
  def _send_request(self, url, method = "get", scope = None, params = None, headers = None, data = None, version = "v1.0", session_config = None, *args, **kwargs):
    """
    This is the direct call to the send request. You have to handel the errors
    """

    if headers is None:
      headers = {}

    if url.startswith("/"):
      url = f'{url[1:]}'
    safe_headers = self.get_common().helper_type().dictionary().merge_dictionary(
      [
        {
          "Content-Type":"application/json"
        },
        headers,
        self._get_auth_header(scope= scope)
      ]
    )

    if session_config is not None:
      session_header = self.generate_session_header(
        session_config= session_config
      )
      
      if session_header is not None:
        safe_headers[session_header["key"]] = session_header["value"]


    graph_url = f'{self.generate_url_prefix(version= version)}{url}{self._process_params(params)}'
    
    try:
      param_data = {
        "url": graph_url,
        "headers": safe_headers
      }

      if data is not None:
        param_data["data"] = self.get_common().helper_json().dumps(data= data) if not self.get_common().helper_type().general().is_type(obj= data, type_check= bytes) else data

      request_response = self._get_request_method(method=method)(**param_data)
      request_response.raise_for_status()

      if request_response.status_code != 204:
        try:
          return request_response.json()
        except Exception as err:
          self.get_common().get_logger().exception(
            msg= f"Exception JSON - Not Caught - could not complete graph request - Status Code {request_response.status_code}\n{request_response.text}\n{err}",
            extra={
              "err": err,
              "url": graph_url,
              "method": method,
              "data": self.get_common().helper_json().dumps(data= data) if data is not None and not self.get_common().helper_type().general().is_type(obj= data, type_check= bytes) else "",
              "headers": self.get_common().helper_json().dumps(data= headers) if headers is not None else "",
              "params": self.get_common().helper_json().dumps(data= params) if params is not None else "",
            }
          )

    except requests.exceptions.HTTPError as err:
      self.get_common().get_logger().exception(
        msg= f"HTTPError - Not Caught - could not complete graph request - Status Code {request_response.status_code}\n{request_response.text}\n{err}",
        extra={
          "err": err,
          "url": graph_url,
          "method": method,
          "data": self.get_common().helper_json().dumps(data= data) if data is not None and not self.get_common().helper_type().general().is_type(obj= data, type_check= bytes) else "",
          "headers": self.get_common().helper_json().dumps(data= headers) if headers is not None else "",
          "params": self.get_common().helper_json().dumps(data= params) if params is not None else "",
        }
      )
      raise err

    except Exception as err:
      
      self.get_common().get_logger().exception(
        msg= f"Exception - Not Caught - could not complete graph request - Status Code {request_response.status_code}\n{request_response.text}\n{err}",
        extra={
          "err": err,
          "url": graph_url,
          "method": method,
          "data": self.get_common().helper_json().dumps(data= data) if data is not None and not self.get_common().helper_type().general().is_type(obj= data, type_check= bytes) else "",
          "headers": self.get_common().helper_json().dumps(data= headers) if headers is not None else "",
          "params": self.get_common().helper_json().dumps(data= params) if params is not None else "",
        }
      )
      raise err