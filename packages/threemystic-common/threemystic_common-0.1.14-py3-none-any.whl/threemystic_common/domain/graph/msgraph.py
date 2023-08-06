from threemystic_common.domain.graph.base_class.base import graph_base as base

# This will probably not be included as it looks like MS has a python SDK
# https://github.com/microsoftgraph/msgraph-sdk-python
# so the sdk is still very much in beta. I do not recommend at this time. - 2023-06-22
class graph_msgraph(base):
  """This is a set of library wrappers to help monitor performance"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"graph_msgraph", *args, **kwargs)    

   
  def graph_scope_default(self, *args, **kwargs):
    return 'https://graph.microsoft.com/.default'
    
  def openid_config_default(self, *args, **kwargs):
    return "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
  
  def generate_url_prefix(self, version = "v1.0", *args, **kwargs):
    return f'https://{self.get_openid_config()["msgraph_host"]}/{version}/'
  
  def create_folder_data(self, name = "New Folder", folder_args = None, *args, **kwargs):
    if not self.get_common().helper_type().general().is_type(obj= folder_args, type_check= dict):
      return {
      "name": name,
      "folder": { }
      }
    
    return self.get_common().helper_type().dictionary().merge_dictionary([
      {},
      {
      "folder": { }
      },
      folder_args,
      {"name": name,}
    ])

  def create_file_data(self, name = "New File", mime_type = "text/plain", file_args = None, *args, **kwargs):
    if not self.get_common().helper_type().general().is_type(obj= file_args, type_check= dict):
      return {
      "name": name,
      "folder": { }
      }
    
    return self.get_common().helper_type().dictionary().merge_dictionary([
      {},
      file_args,
      {
        "name": name,
        "file": { 
          "mimeType": mime_type
        }
      }
    ])
  
  def _get_known_session_types(self, *args, **kwargs):
    return {
      "workbook": "Workbook"
    }
  
  def get_known_session_types(self, *args, **kwargs):
    return list(self._get_known_session_types().keys())
  
  def __get_session_key_value(self, session_config, *args, **kwargs):
    session_type= self.get_common().helper_type().string().set_case(string_value= session_config.get("type"), case= "lower")

    if session_type not in self.get_known_session_types():
      return None
    
    if session_type == "workbook":

      session_key = {
        "drive_item_id": session_config.get("drive_id"), 
        "persist_changes": session_config.get("persist_changes"),
        "type": self._get_known_session_types().get(session_type)
      } 

    if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= session_config.get("graph_resource_id")):
      session_key["graph_resource_id"] = session_config.get("graph_resource_id")

    return self.get_common().helper_json().dumps(data= session_key)
  
  def _generate_session_data(self, session_config, refresh= False, refresh_session = False, closing_session = False, *args, **kwargs):
    if refresh_session and not refresh:
      refresh = True
    
    session_type= self.get_common().helper_type().string().set_case(string_value= session_config.get("type"), case= "lower")

    if session_type not in self.get_known_session_types():
      return None
    
    base_path = ""
    if session_type == "workbook":
      base_path = f"{session_config.get('drive_id')}" if self.get_common().helper_type().string().set_case(string_value= session_config.get("graph_resource"), case= "lower") == "me" else f"items/{session_config.get('drive_id')}"
      base_path = f"drive/{base_path}/workbook"


    session_key = self.__get_session_key_value(session_config= session_config)
    if hasattr(self, "_ms_graph_sessions") and not refresh:
      if self._ms_graph_sessions.get(session_key):
        return {
          "type": session_type,
          "data": self._ms_graph_sessions.get(session_key) if not closing_session else self._ms_graph_sessions.pop(session_key),
          "base_path": base_path
        }
      
    if not hasattr(self, "_ms_graph_sessions"):
      self._ms_graph_sessions = {}
    
    try:
      response =  self._send_request(
        url = self.generate_graph_url(
          resource= session_config.get("graph_resource"), 
          resource_id= session_config.get('graph_resource_id'), 
          base_path= f"{base_path}{'/createSession' if not refresh_session else '/refreshSession'}"),
          data = { "persistChanges": session_config.get("persist_changes") } if not refresh_session else None,
          headers= {} if not refresh_session else { f'{session_type}-Session-Id': self._ms_graph_sessions.get(session_key).get("data")["id"]},
          method= "post"
      )
    except Exception as err:
      if refresh_session:
        return self._generate_session_data(session_config= session_config, refresh= True, refresh_session = False, *args, **kwargs)
      raise err
    if not refresh_session:
      self._ms_graph_sessions[session_key] = response

    return self._generate_session_data(session_config= session_config, refresh= False, refresh_session = False, *args, **kwargs)
      
  def generate_session_header(self, session_config, refresh= False, refresh_session = False, *args, **kwargs):
    header_data = self._generate_session_data(
      session_config= session_config,
      refresh= refresh,
      refresh_session= refresh_session,
      *args, **kwargs
    )
    if header_data is None:
      return None
    
    return {
      "key": f'{header_data.get("type")}-Session-Id',
      "value": header_data.get("data")["id"]
    }

  def close_session(self, session_config, refresh = False, *args, **kwargs):
    header_data = self._generate_session_data(
      session_config= session_config,
      refresh= refresh,
      closing_session= True,
      *args, **kwargs
    )
    if header_data is None:
      return None

    return self.send_request(
      url = self.generate_graph_url(
        resource= session_config.get("graph_resource"), 
        resource_id= session_config.get("graph_resource_id"), 
        base_path= f"{header_data.get('base_path')}/closeSession",
      ),
      headers= {"workbook-session-id": header_data.get("data")["id"]},
      method= "post"
    )
     
       

  def generate_graph_url(self, resource, resource_id = None, base_path= None, *args, **kwargs):
    graph_url = self.get_common().helper_type().string().trim(string_value= f'{resource}')
    if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= resource_id):
      resource_id = self.get_common().helper_type().string().ltrim(string_value= resource_id, trim_chars= "\\/" )
      graph_url = self.get_common().helper_type().string().rtrim(string_value= f'{graph_url}/{resource_id}', trim_chars= "\\/")
    
    if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= base_path):
      base_path = self.get_common().helper_type().string().ltrim(string_value= base_path, trim_chars= "\\/" )
      graph_url = self.get_common().helper_type().string().rtrim(string_value= f'{graph_url}/{base_path}', trim_chars= "\\/")

    return graph_url
  
  def _get_auth_header(self, scope= None, refresh = False, *args, **kwargs):
    if self.get_common().helper_type().string().is_null_or_whitespace(string_value= scope):
      scope = self.graph_scope
    
    scope_hash =self.get_common().encryption().hash(hash_method= "sha1").generate_hash(data= scope)
    if hasattr(self, "_current_graph_token") and not refresh:
      if self._current_graph_token.get(scope_hash) is not None:
        if not self.get_common().helper_type().datetime().is_token_expired_epoch(
          token_life_duration= self.get_common().helper_type().datetime().time_delta(
            seconds= self._current_graph_token.get(scope_hash).get("expires_on")
          )):
          return {
            "Authorization": f'Bearer {self._current_graph_token.get(scope_hash)["token"]}'
          }
    
    if not hasattr(self, "_current_graph_token"):
      self._current_graph_token = {}
    
    auth_token = (self.graph_credentials.get_token(scope)
                  if not self.get_common().helper_type().general().is_type(obj= self.graph_credentials, type_check= dict)
                  else self.graph_credentials.get("get_token"))

    self._current_graph_token[scope_hash] = ({
      "token": auth_token.token,
      "expires_on": auth_token.expires_on
    } if not self.get_common().helper_type().general().is_type(obj= auth_token, type_check= dict)
    else auth_token
    )
    return self._get_auth_header(scope= scope, *args, **kwargs)
  
  def _get_session_type(self, session_type, *args, **kwargs):
    if self.get_common().helper_type().string().is_null_or_whitespace(string_value= session_type):
      return None

    session_type= self.get_common().helper_type().string().set_case(string_value= session_type, case= "lower")
    if session_type in self.get_known_session_types():
      return self._get_known_session_types()[session_type]
    
    
    raise self.get_common().exception().exception(
      exception_type = "argument"
    ).type_error(
      logger = self.get_common().get_logger(),
      name = "type",
      message = f"type is an unknown value ({session_type}): valid options {self.get_known_session_types()}"
    )