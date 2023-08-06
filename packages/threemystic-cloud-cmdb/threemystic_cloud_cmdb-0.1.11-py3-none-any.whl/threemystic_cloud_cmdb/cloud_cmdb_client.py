from threemystic_cloud_cmdb.cloud_providers.base_class.base import cloud_cmdb_provider_base as base
from threemystic_cloud_data_client.cloud_data_client import cloud_data_client

class cloud_cmdb_client(base): 
  """This is a library to help with the interaction with the cloud providers"""

  def __init__(self, logger = None, common = None, *args, **kwargs) -> None: 
    super().__init__(provider= "", common= common, logger_name= "cloud_cmdb_client", logger= logger, *args, **kwargs)
    
  def version(self, *args, **kwargs):
    if hasattr(self, "_version"):
      return self._version
    import threemystic_cloud_cmdb.__version__ as __version__
    self._version = __version__.__version__
    return self.version()
    
  def get_supported_providers(self, *args, **kwargs):
    return super().get_supported_providers()
    return super().get_supported_providers()
  
  def init_client(self, provider, *args, **kwargs):
    provider = self.get_common().helper_type().string().set_case(string_value= provider, case= "lower") if provider is not None else ""

    if provider not in self.get_supported_providers():
      raise self.get_common().exception().exception(
        exception_type = "argument"
      ).not_implemented(
        logger = self.get_common().get_logger(),
        name = "provider",
        message = f"Unknown Cloud Provided: {provider}.\nSupported Cloud Providers{self.get_supported_providers()}"
      )

    if not hasattr(self, "_client"):
      self._client = {}

    if self._client.get(provider) is not None:
      return

    if provider == "azure":      
      from threemystic_cloud_cmdb.cloud_providers.azure.client import cloud_cmdb_azure_client as provider_cloud_cmdb
      self._client[provider] = provider_cloud_cmdb(
        cloud_cmdb = self,
        cloud_data_client= cloud_data_client(
          provider= provider,
          logger= self.get_logger(), 
          common= self.get_common()
        ),
      )
      return
    
    if provider == "aws":
      from threemystic_cloud_cmdb.cloud_providers.aws.client import cloud_cmdb_aws_client as provider_cloud_cmdb
      self._client[provider] = provider_cloud_cmdb(
        cloud_cmdb = self,
        cloud_data_client= cloud_data_client(
          provider= provider,
          logger= self.get_logger(), 
          common= self.get_common()
        ),
      )
      return  
       
    raise self.get_common().exception().exception(
      exception_type = "argument"
    ).not_implemented(
      logger = self.get_common().get_logger(),
      name = "provider",
      message = f"Unknown Cloud Provided: {provider}.\nSupported Cloud Providers{self.get_supported_providers()}"
    )

  def client(self, provider = None, *args, **kwargs):
    if self.get_common().helper_type().string().is_null_or_whitespace(string_value= provider):
      provider = self.get_default_provider()
      if self.get_common().helper_type().string().is_null_or_whitespace(string_value= provider):
        raise self.get_common().exception().exception(
          exception_type = "argument"
        ).not_implemented(
          logger = self.get_common().get_logger(),
          name = "provider",
          message = f"provider cannot be null or whitespace"
        )
  
    provider = self.get_common().helper_type().string().set_case(string_value= provider, case= "lower")
    if not hasattr(self, "_client"):
      self.init_client(provider= provider,  *args, **kwargs)
      return self.client(provider= provider, *args, **kwargs)
    
    return self._client.get(provider)

  