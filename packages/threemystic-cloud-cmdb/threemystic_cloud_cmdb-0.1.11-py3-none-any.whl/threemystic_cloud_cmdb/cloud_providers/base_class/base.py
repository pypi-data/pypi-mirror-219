from threemystic_common.base_class.base_provider import base
from threemystic_cloud_cmdb.cli import cloud_cmdb_cli
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers
from threemystic_cloud_data_client.cloud_providers.base_class.base import cloud_data_client_provider_base as main_cloud_data_client

class cloud_cmdb_provider_base(base):
  def __init__(self, *args, **kwargs):
    if "provider" not in kwargs:
      kwargs["provider"] = self.get_default_provider()
    super().__init__(*args, **kwargs)
    
  def _setup_another_config(self):
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "repeat_config": {
            "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
            "messages":{
              "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
            },
            "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
            "desc": f"Do you want to setup another provider?: {self.get_common().helper_type().bool().is_true_values()}",
            "default": None,
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": True
        }
      }
    )

    if response is None:
      return
    
    if response.get("repeat_config") is None:
      return
    
    if response.get("repeat_config").get("formated") is not True:
      return
    
    print()
    print()
    print("-------------------------------------------------------------------------")
    print()
    print()

    cloud_cmdb_cli().process_client_action("config")
  
  def update_general_config_completed(self, status, *args, **kwargs):
    self.get_config()["_config_process"] = status
    self._save_config()
  
  def is_data_client_config_completed(self, *args, **kwargs):
    cloud_client = main_cloud_data_client( common= self.get_common(), logger_name= "cmdb_init", logger= self.get_common().get_logger())
    
    return cloud_client.is_general_config_completed()

  
  def ensure_data_client_config_completed(self, *args, **kwargs):
    if self.is_data_client_config_completed():
      return True
    
    print("Data Client needs to be configured")
    cloud_client = main_cloud_data_client( common= self.get_common(), logger_name= "cmdb_init", logger= self.get_common().get_logger())
    cloud_client._setup_another_config(force_config= True)
    
    return False

    
  def is_general_config_completed_only(self, *args, **kwargs):
    return self.get_config().get("_config_process") is True

  def is_general_config_completed(self, *args, **kwargs):
    return self.is_general_config_completed_only() and self.is_data_client_config_completed()
    
  
  def get_main_directory_name(self, *args, **kwargs):
    return "cmdb"  
  
  def get_supported_cloud_share(self, *args, **kwargs):
    return ["ms365"]

  def __load_config(self, *args, **kwargs):
    config_data = self.get_common().helper_config().load(
      path= self.config_path(),
      config_type= "yaml"
    )
    if config_data is not None:
      return config_data
    
    return {}

  def get_cmdb_report_path(self, *args, **kwargs):
    local_path = self.get_config_value("default_cmdb_report_path", self.default_report_path())
    if self.get_common().helper_type().string().is_null_or_whitespace(string_value= local_path):
      local_path = self.default_report_path()
    if self.get_common().helper_path().is_valid_filepath(path= local_path):
      local_path = self.get_common().helper_path().get(path= local_path)
      if not local_path.exists():
        local_path.mkdir(parents= True)
      
      return self.get_common().helper_path().expandpath_user(path= local_path)
    
    return self.get_common().helper_path().expandpath_user(path= self.default_report_path())

  def default_report_path(self, *args, **kwargs):
    return self.get_common().get_threemystic_public_directory().joinpath(f"{self.get_main_directory_name()}/reports")
  
  def config_path(self, *args, **kwargs):
    return self.get_common().get_threemystic_directory_config().joinpath(f"{self.get_main_directory_name()}/config")
  
  def reset_config_tag_data(self, *args, **kwargs):    
    self.get_config()["tag_data"] = {}
    self._save_config()

  def has_tag_data_config(self, refresh = False, *args, **kwargs):
    
    if len(self.get_config_tag_data(refresh= refresh)) < 1:
      return False

    return True

  def get_config_tag_data(self, refresh = False, *args, **kwargs):
    if self.get_config(refresh= refresh).get("tag_data") is not None:
      return self.get_config().get("tag_data")
    
    self.get_config()["tag_data"] = {}
    self._save_config()
     
    return self.get_config_tag_data(*args, **kwargs)

  def _update_config_tag_data(self,config_key, config_value, refresh = False,  *args, **kwargs):
     self.get_config_tag_data(refresh = refresh)[config_key] = config_value
     
  def _save_config_tag_data(self, *args, **kwargs):
     self._save_config()
  
  def get_tag_data_config_value(self, config_key, default_if_none = None, refresh = False, *args, **kwargs):
    config_value = self.get_config_tag_data(refresh= refresh).get(config_key)
    if config_value is not None:
      return config_value
    
    return default_if_none
  
  def reset_config_cloud_share(self, *args, **kwargs):    
    self.get_config()["cloud_share"] = {}
    self._save_config()

  def has_cloud_share_configured(self, refresh = False, *args, **kwargs):
    
    if len(self.get_config_cloud_share(refresh= refresh)) < 1:
      return False

    if (not self.get_common().helper_type().string().is_null_or_whitespace(
          string_value= self.get_config_cloud_share().get("type")) and
        self.get_config_cloud_share().get("type") in self.get_supported_cloud_share()):
      return True
    
    return False

  def get_config_cloud_share(self, refresh = False, *args, **kwargs):
    if self.get_config(refresh= refresh).get("cloud_share") is not None:
      return self.get_config().get("cloud_share")
    
    self.get_config()["cloud_share"] = {}
    self._save_config()
     
    return self.get_config_cloud_share(*args, **kwargs)

  def _update_config_cloud_share(self,config_key, config_value, refresh = False,  *args, **kwargs):
     self.get_config_cloud_share(refresh = refresh)[config_key] = config_value
     
  def _save_config_cloud_share(self, *args, **kwargs):
     self._save_config()
  
  def get_cloud_share_config_value(self, config_key, default_if_none = None, refresh = False, *args, **kwargs):
    config_value = self.get_config_cloud_share(refresh= refresh).get(config_key)
    if config_value is not None:
      return config_value
    
    return default_if_none
  
  def get_config(self, refresh = False, *args, **kwargs):
    if hasattr(self, "_config_data") and not refresh:
      return self._config_data
    
    self._config_data = self.__load_config()    
    return self.get_config(*args, **kwargs)

  def _update_config(self,config_key, config_value, refresh= False,  *args, **kwargs):
     self.get_config(refresh = refresh)[config_key] = config_value
     
  def _save_config(self, *args, **kwargs):
     if not self.config_path().parent.exists():
       self.config_path().parent.mkdir(parents= True)
     self.config_path().write_text(
      data= self.get_common().helper_yaml().dumps(data= self.get_config())
     )
     self.get_config(refresh = True) 
  
  def get_config_value(self, config_key, default_if_none = None, refresh = False, *args, **kwargs):
    config_value = self.get_config(refresh= refresh).get(config_key)
    if config_value is not None:
      return config_value
    
    return default_if_none
  
  def get_default_provider(self, refresh = False, *args, **kwargs):
    return self.get_config(refresh= refresh).get("default_provider")
  
  def set_default_provider(self, value, refresh = False, *args, **kwargs):
    self.get_config(refresh= refresh)["default_provider"] = value
    self._save_config()

  def action_config(self, *args, **kwargs):
    print("Provider config not configured")

  def action_data(self, *args, **kwargs):
    print("Provider config not configured")
  
  
    

  
  

