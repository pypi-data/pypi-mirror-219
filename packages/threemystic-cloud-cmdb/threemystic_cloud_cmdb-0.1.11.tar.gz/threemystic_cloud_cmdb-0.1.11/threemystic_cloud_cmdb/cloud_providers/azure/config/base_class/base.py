from threemystic_cloud_cmdb.cloud_providers.azure.base_class.base import cloud_cmdb_provider_azure_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers

class cloud_cmdb_azure_config_base(base):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def step(self, *args, **kwargs):
    return self.ensure_data_client_config_completed()