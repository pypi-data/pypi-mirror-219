from threemystic_cloud_cmdb.cloud_providers.base_class.base_client import cloud_cmdb_provider_base_client as base


class cloud_cmdb_azure_client(base):
  def __init__(self, *args, **kwargs):
    super().__init__(provider= "azure", logger_name= "cloud_cmdb_azure_client", *args, **kwargs)
    
