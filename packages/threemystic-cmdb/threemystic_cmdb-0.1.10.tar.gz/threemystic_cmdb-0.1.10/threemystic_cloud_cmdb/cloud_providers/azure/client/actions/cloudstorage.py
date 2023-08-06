from threemystic_cloud_cmdb.cloud_providers.azure.client.actions.base_class.base import cloud_cmdb_azure_client_action_base as base
import asyncio
from azure.mgmt.storage import StorageManagementClient
from decimal import Decimal, ROUND_HALF_UP

class cloud_cmdb_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="cloudstorage", 
      logger_name= "cloud_cmdb_azure_client_action_cloudstorage", 
      uniqueid_lambda = lambda: True
      *args, **kwargs)
  
  def _load_cmdb_general_data(self, *args, **kwargs):
    if hasattr(self, "_cmdb_general_data_loaded"):
      return self._cmdb_general_data_loaded
    
    self._cmdb_general_data_loaded = {
      self.get_cmdb_data_action():{
        "display":"CloudStorage",
      }
    }
    return self._load_cmdb_general_data()
  
  def _load_cmdb_column_data(self, *args, **kwargs):
    if hasattr(self, "_cmdb_column_data_loaded"):
      return self._cmdb_column_data_loaded
    
    self._cmdb_column_data_loaded = {
      self.get_cmdb_data_action(): {
        "Service":{
          "display": "Service",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["extra_storage_account","sku","name"])
        },
        "BucketContainer":{
          "display": "BucketContainer",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["extra_storage_account","name"])
        },
        "BucketName":{
          "display": "BucketName",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["name"])
        },
        "AvgSizeLast24HR_Bytes":{
          "display": "AvgSizeLast24HR_Bytes",
          "handler": lambda item:  self.get_item_data_value(item_data= item, value_key=["extra_storageaccount_bytes_24hours"])
        },
        "SampleObjectClass":{
          "display": "SampleObjectClass",
          "handler": lambda item: None
        },
        "SampleObjectRetention":{
          "display": "SampleObjectRetention",
          "handler": lambda item: None
        },
        "Encryption":{
          "display": "Encryption",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["extra_storage_account", "encryption", "services", "blob", "enabled"])
        },
        "Versioning":{
          "display": "Versioning",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["extra_storage_account", "immutable_storage_with_versioning"])
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: self.generate_resource_tags_csv(tags= self.get_item_data_value(item_data= item, value_key=["extra_storage_account", "tags"]))
        },
      } 
    }
    return self._load_cmdb_column_data()