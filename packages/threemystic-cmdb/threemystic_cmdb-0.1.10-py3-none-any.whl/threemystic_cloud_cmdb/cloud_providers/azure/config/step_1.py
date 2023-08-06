from threemystic_cloud_cmdb.cloud_providers.azure.config.base_class.base import cloud_cmdb_azure_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers



class cloud_cmdb_azure_config_step_1(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_azure_config_step_1", *args, **kwargs)
    
  def check_cloud_data_client(self, *args, **kwargs):
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "base_config": {
          "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
          "messages":{
            "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
          },
          "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
          "desc": f"Do you need to configure the Cloud Data Client.\nValid Options: {self.get_common().helper_type().bool().is_true_values()}",
          "default": None,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": True
        }
      }
    )

    if response is None:
      return
    
    if not self.get_common().helper_type().bool().is_true(check_value= response.get("base_config").get("formated")):
      return
    
    from threemystic_cloud_data_client.cloud_providers.aws import cloud_data_client_aws as client
    client(common= self.get_common(), logger= self.get_common().get_logger()).action_config()
    

  def step(self, *args, **kwargs):
    
    if not super().step(run_base_config= True):
      return
    
    print()
    print()
    print()
    print(f"No additional config is required at this time for CMDB Client: {self.get_provider()}")

    self.check_cloud_data_client(*args, **kwargs)

    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "base_config": {
          "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
          "messages":{
            "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
          },
          "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
          "desc": f"CMDB Client: Do you want to configure base config?\nLeave blank to exit.\nValid Options: {self.get_common().helper_type().bool().is_true_values()}",
          "default": None,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": True
        }
      }
    )

    if response is None:
      return
    
    if not self.get_common().helper_type().bool().is_true(check_value= response.get("base_config").get("formated")):
      return
    
    from threemystic_cloud_cmdb.cloud_providers.general  import cloud_cmdb_general as client
    client(common= self.get_common()).action_config()
    
    
  
