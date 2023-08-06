from threemystic_cloud_cmdb.cloud_providers.base_class.base import cloud_cmdb_provider_base as base

class cloud_cmdb_provider_aws_base(base):
  def __init__(self, *args, **kwargs):
    super().__init__(provider= "aws", *args, **kwargs)  
