from threemystic_cloud_cmdb.cloud_providers.base_class.base_cmdb import cloud_cmdb_provider_base_cmdb as base

class cloud_cmdb_azure_client_action_base(base):
  def __init__(self, *args, **kwargs):
    super().__init__(provider= "azure", *args, **kwargs)  
  
  def _get_default_columns_raw(self, *args, **kwargs):    
    if hasattr(self, "_columns_raw"):
      return self._columns_raw
    self._columns_raw = [
      {
        "id":  "TenantId",
        "display": "TenantId",
        "handler": lambda item: self.get_cloud_client().get_tenant_id(tenant= item["account"], is_account= True),
        "cmdb": {
          "hidden": True
        }
      },
      {
        "id":  "AccountId",
        "display": "SubscriptionId",
        "handler": lambda item: self.get_cloud_client().get_account_id(account = item["account"]),
        "cmdb": {
          "display": "AccountId",
        }
      },
      {
        "id":  "Account",
        "display": "Subscription",
        "handler": lambda item: self.get_cloud_client().get_account_name(account = item["account"]),
        "cmdb": {
          "display": "Account",
          "handler": lambda item: f'{self.get_cloud_client().get_account_name(account = item["account"])} / {self.get_cloud_client().get_tenant_id(tenant = item["account"], is_account= True)}'
        }
      }
    ]

    return self._get_default_columns_raw()

  
  def generate_resource_tags_csv(self, tags, seperator=",", tag_attribute_seperator=":", **kwargs):
    if tags is None:
      return None
    return seperator.join([f"{key}{tag_attribute_seperator}{tag}" for key,tag in tags.items()])
  
  def generate_tag_columns(self, account, resource, is_cmdb= False, *args, **kwargs):
    if not is_cmdb:
      return []

    return {}
  # if InventoryDataSheet.get("include_requiredtags") is None or InventoryDataSheet.get("include_requiredtags").get("include") != True or tags is None or len(tags) < 1:
  #     return []
    
  #   tags_keyed = cls.get_tags_as_dict(tags)
  #   required_tags = cls.required_tag_names()

  #   tags_keys_lower = {}
  #   for key in tags_keyed.keys():
  #     if key.lower() in tags_keys_lower:
  #       continue
      
  #     tags_keys_lower[key.lower()] = key

  #   return_tag_data = {tag:"" for tag in required_tags}
  #   if cls.is_type(tags, dict):
  #     tags = [{"Key": tag, "Value": value} for tag, value in tags.items() ]

  #   for tag, alt_tags in required_tags.items():
  #     if alt_tags is None:
  #       alt_tags = []

  #     if cls.is_type(alt_tags, dict):
  #       cls.generate_tag_columns_basic(return_tag_data, alt_tags["basic"], tags_keyed, tag)
  #       for custom_tag in alt_tags["custom"]:
  #         tags_keyed_custom = custom_tag
  #         if cls.isNullOrWhiteSpace(tags_keyed.get(custom_tag)):
  #           if not custom_tag.lower() in tags_keys_lower:
  #             continue
  #           tags_keyed_custom = tags_keys_lower[custom_tag.lower()]
            

  #         return_tag_data[tag] = alt_tags["custom"][custom_tag](tags_keyed[tags_keyed_custom])
  #       continue

  #     alt_tags.insert(0, tag)
  #     return_tag_data[tag] = cls.generate_tag_columns_basic(return_tag_data, alt_tags, tags_keyed, tag)

      
  #   return [val for val in return_tag_data.values()]

  def _get_report_default_row(self, account, *args, **kwargs):
    return [
      column.get("handler")({"account": account}) for column in self._get_default_columns_raw()
    ]
  
  def _get_report_default_row_cmdb(self, account, *args, **kwargs):
    return_data = {}
    for column in self._get_default_columns_raw():
      if self.get_ishidden_column_data(column_data= column, is_cmdb= True):
        continue

      return_data[column.get("id")] = self.get_handler_column_data(column_data= column, is_cmdb= True)({"account": account})
    
    return return_data
