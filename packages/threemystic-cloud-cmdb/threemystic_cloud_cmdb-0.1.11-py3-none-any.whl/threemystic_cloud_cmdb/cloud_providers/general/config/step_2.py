from threemystic_cloud_cmdb.cloud_providers.general.config.base_class.base import cloud_cmdb_general_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers



class cloud_cmdb_general_config_step_2(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_general_config_step_2", *args, **kwargs)
    

  def step(self, *args, **kwargs):
    if not super().step(run_base_config= True):
      return
    
    
    print("-----------------------------")
    print()
    print()
    print("CMDB Cloud Share")
    print()
    print()
    print("-----------------------------")
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "cmdb_cloud_share": {
          "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
          "messages":{
            "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
          },
          "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
          "desc": f"Do you want to save the CMDB in a cloud Share?\nValid Options: {self.get_common().helper_type().bool().is_true_values()}",
          "default": len(self.get_config_cloud_share()) > 0,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": len(self.get_config_cloud_share()) > 0
        }
      }
    )
    
    if response is None:
      return

    if not self.get_common().helper_type().bool().is_true(check_value= response.get("cmdb_cloud_share").get("formated")):
      from threemystic_cloud_cmdb.cloud_providers.general.config.step_3 import cloud_cmdb_general_config_step_3 as step
      next_step = step(common= self.get_common(), logger= self.get_logger())
      
      if not self.is_general_config_completed_only():
        self.update_general_config_completed(status= "step2")

      if len(self.get_config_cloud_share()) < 1:
        next_step.step(cloud_share= self.get_cloud_share_config_value(config_key= "type"))
        return
      
      response = self.get_common().generate_data().generate(
        generate_data_config = {
          "reset_cloud_share": {
            "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
            "messages":{
              "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
            },
            "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
            "desc": f"Are you sure want to stop cloud share feature?\nValid Options: {self.get_common().helper_type().bool().is_true_values()}",
            "default": None,
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": True
          }
        }
      )
      if response is None:
        next_step.step(cloud_share= self.get_cloud_share_config_value(config_key= "type"))

      if self.get_common().helper_type().bool().is_true(check_value= response.get("reset_cloud_share").get("formated")):
        self.reset_config_cloud_share()
      
      next_step.step(cloud_share= self.get_cloud_share_config_value(config_key= "type"))
      return

    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "type": {
          "validation": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower") in self.get_supported_cloud_share(),
          "messages":{
            "validation": f"Valid options are: {self.get_supported_cloud_share()}",
          },
          "conversion": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower"),
          "desc": f"What is the cloud share you would like to use? \nValid Options: {self.get_supported_cloud_share()}",
          "default": self.get_cloud_share_config_value(
            config_key= "type"
          ),
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": not self.get_common().helper_type().string().is_null_or_whitespace(string_value= self.get_cloud_share_config_value(
            config_key= "type"
          ))
        },
        "name": {
          "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) and self.get_common().helper_path().is_valid_filename(file_name= item),
          "messages":{
            "validation": f"Valid options are: {self.get_supported_cloud_share()}",
          },
          "conversion": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower"),
          "desc": f"What is the name you would like to use for the cmdb (no extension)? The name will be converted to all lowercase.",
          "default": self.get_cloud_share_config_value(
            config_key= "name", default_if_none= "cmdb"
          ),
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": True
        },
      }
    )
    
    if(response is not None):
      for key, item in response.items():
        self._update_config_cloud_share(config_key= key, config_value= item.get("formated"))    
      if self.get_cloud_share_config_value(config_key= response.get("type").get("formated")) is None:
        self._update_config_cloud_share(config_key= response.get("type").get("formated"), config_value= {})
      self._save_config_cloud_share()
      
      
      from threemystic_cloud_cmdb.cloud_providers.general.config.step_2_cloud_share import cloud_cmdb_general_config_step_2_cloud_share as step
      next_step = step(common= self.get_common(), logger= self.get_logger())
      
      if not self.is_general_config_completed_only():
        self.update_general_config_completed(status= "step2")
        
      next_step.step(cloud_share= self.get_cloud_share_config_value(config_key= "type"))

      print("-----------------------------")
      print()
      print()
      print("CMDB Cloud Share is updated")
      print()
      print()
      print("-----------------------------")
    else:
      print("-----------------------------")
      print()
      print()
      print("CMDB Cloud Share NOT updated")
      print()
      print()
      print("-----------------------------")

    
    
  
