from threemystic_cloud_cmdb.cloud_providers.general.config.base_class.base import cloud_cmdb_general_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers


class cloud_cmdb_general_config_step_3(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_general_config_step_3", *args, **kwargs)
    

  def step(self, *args, **kwargs):
    if not super().step(run_base_config= True):
      return
    
    self.update_general_config_completed(status= True)
    
    # response = self.get_common().generate_data().generate(
    #   generate_data_config = {
    #     "reset_cloud_share": {
    #       "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
    #       "messages":{
    #         "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
    #       },
    #       "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
    #       "desc": f"Are you sure want to stop cloud share feature?\nValid Options: {self.get_common().helper_type().bool().is_true_values()}",
    #       "default": None,
    #       "handler": generate_data_handlers.get_handler(handler= "base"),
    #       "optional": True
    #     }
    #   }
    # )
    # if response is None:
    #   next_step.step(cloud_share= self.get_cloud_share_config_value(config_key= "type"))

    # if self.get_common().helper_type().bool().is_true(check_value= response.get("reset_cloud_share").get("formated")):
    #   self.reset_config_cloud_share()
    
    # next_step.step(cloud_share= self.get_cloud_share_config_value(config_key= "type"))
    # return

    if self.has_tag_data_config():
      return self.step_edit_existing()
    
  def step_new_tag(self, *args, **kwargs):
    pass
    
  def step_edit_existing(self, *args, **kwargs):
    pass