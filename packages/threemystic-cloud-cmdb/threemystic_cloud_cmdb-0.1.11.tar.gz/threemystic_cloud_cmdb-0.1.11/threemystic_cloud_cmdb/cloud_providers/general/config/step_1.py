from threemystic_cloud_cmdb.cloud_providers.general.config.base_class.base import cloud_cmdb_general_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers
from threemystic_common.base_class.base_script_options import base_process_options
import textwrap, argparse
from time import sleep


class cloud_cmdb_general_config_step_1(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_general_config_step_1", *args, **kwargs)

    self._process_cli_args()
    
  def _process_cli_args(self, *args, **kwargs):
    process_options = base_process_options(common= self.get_common())
    token_parser_args = { 
    }
    self._arg_parser = process_options.get_parser(
      parser_init_kwargs = {
        "prog": "3mystic_cloud_cmdb --config",
        "formatter_class": argparse.RawDescriptionHelpFormatter,
        "description": textwrap.dedent('''\
        Once the config has been completed once you can skip steps.
        '''),
        "add_help": False,
        "epilog": ""
      },
      parser_args = self.get_common().helper_type().dictionary().merge_dictionary([
        {},
        token_parser_args,
        {
          "--step2": {
            "default": None,             
            "const": "step_2",
            "dest": "config_step",
            "help": "Skip to Step 2",
            "action": 'store_const'
          },
          # "--step3": {
          #   "default": None,             
          #   "const": "step_3",
          #   "dest": "config_step",
          #   "help": "Skip to Step 3",
          #   "action": 'store_const'
          # }
        },
      ])
    )


    processed_info = process_options.process_opts(
      parser = self._arg_parser
    )
    
    self._processed_arg_info = processed_info.get("processed_data")
    

  def step(self, *args, **kwargs):
    if not super().step(run_base_config= True):
      return
    
    if self.is_general_config_completed_only():
      if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= self._processed_arg_info.get("config_step")):
        step_action = __import__(f'threemystic_cloud_cmdb.cloud_providers.general.config.{self._processed_arg_info.get("config_step")}', fromlist=[f'cloud_cmdb_general_config_{self._processed_arg_info.get("config_step")}'])
        getattr(step_action, f'cloud_cmdb_general_config_{self._processed_arg_info.get("config_step")}')(
          common= self.get_common(), logger= self.get_logger()
        ).step()
        return
      print("Skip to a later step using the --stepX flag")
      self._arg_parser.print_usage()

    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "default_provider": {
            "validation": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower") in self.get_supported_providers(),
            "messages":{
              "validation": f"Valid options are: {self.get_supported_providers()}",
            },
            "conversion": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower"),
            "desc": f"What do you want as the the default provider? \nValid Options: {self.get_supported_providers()}",
            "default": self.get_default_provider(),
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": not self.get_common().helper_type().string().is_null_or_whitespace(string_value= self.get_default_provider())
        },
        "default_cmdb_report_path": {
            "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) and self.get_common().helper_path().is_valid_filepath(path= item),
            "messages":{
              "validation": f"A valid path is required",
            },
            "conversion": lambda item: item,
            "desc": f"Where should the reports be saved locally?",
            "default": self.get_cmdb_report_path().absolute().as_posix(),
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": True
        }
      }
    )

    if(response is not None):
      for key, item in response.items():
        self._update_config(config_key= key, config_value= item.get("formated"))
      self._save_config()
      print("-----------------------------")
      print()
      print()
      print("Base Configuration is updated")
      print()
      print()
      print("-----------------------------")
      from threemystic_cloud_cmdb.cloud_providers.general.config.step_2 import cloud_cmdb_general_config_step_2 as step
      next_step = step(common= self.get_common(), logger= self.get_logger())
      
      if not self.is_general_config_completed_only():
        self.update_general_config_completed(status= "step1")
      next_step.step()
    else:
      print("-----------------------------")
      print()
      print()
      print("Base Configuration NOT updated")
      print()
      print()
      print("-----------------------------")    
    
    
    

    
    
  
