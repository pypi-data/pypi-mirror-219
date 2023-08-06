from threemystic_cloud_cmdb.cli.actions.base_class.base import cloud_cmdb_action_base as base


class cloud_cmdb_config(base):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


  def _process_provider_aws(self, *args, **kwargs):
      from threemystic_cloud_cmdb.cloud_providers.aws  import cloud_cmdb_aws as client
      client(common= self._cloud_cmdb_client.get_common()).action_config()


  def _process_provider_azure(self, *args, **kwargs):
      from threemystic_cloud_cmdb.cloud_providers.azure import cloud_cmdb_azure as client
      client(common= self._cloud_cmdb_client.get_common()).action_config()

      

  
