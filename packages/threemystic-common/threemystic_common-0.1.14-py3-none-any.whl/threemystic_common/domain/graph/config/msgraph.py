class msgraph_config():
  def __init__(self, 
    common,
    get_token = None,
    default_scopes = None,
  ):  
    
    self.common = common
    self.default_scopes = default_scopes
    self.refresh_token = get_token
    self.__token = None


  def get_token(self, force_refresh = False):
    """
    This method will look to see if the existing token is expired, if so it will refresh the token.
    """

    if not force_refresh and not self.__token is None:
      if not self.__token.get("expiresOn") is None:
        if not self.common.helper_type().datetime().is_token_expired_now(self.common.helper_type().datetime().parse_iso(self.__token["expiresOn"])):
          return self.__token

    self.__token = self.refresh_token()
    return self.__token