from threemystic_cloud_cmdb.cloud_providers.base_class.base import cloud_cmdb_provider_base as base
from abc import abstractmethod
from decimal import Decimal
from math import floor

class cloud_cmdb_general_cmdb_connector_base(base):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__set_cloud_client(*args, **kwargs)
    self.__set_cmdb_data_containers(*args, **kwargs)
    self.__set_cmdb_data_containers_columns(*args, **kwargs)
    self.__set_cmdb_postfix_columns(*args, **kwargs)

    if(self.has_cloud_share_configured()):
      self._validate_cmdb_init()

  @abstractmethod
  def get_existing_columns_sorted_by_index(self, *args, **kwargs):
    pass

  @abstractmethod
  def get_cloud_share(self, *args, **kwargs):
    pass

  @abstractmethod
  def _validate_cmdb_init(self, *args, **kwargs):
    pass

  @abstractmethod
  def _sync_data(self, *args, **kwargs):
    pass
  
  def _get_delete_time(self, *args, **kwargs):
    if hasattr(self, "_general_delete_time"):
      return self._general_delete_time
    
    self._general_delete_time = self.get_common().helper_type().datetime().get()
    return self._get_delete_time()
  def _get_number_of_groups_batchsize(self, total_items,  batch_size = 500, *args, **kwargs):
    groups = total_items / Decimal(batch_size)
    return int(floor(groups)) + 1

  def _get_cmdb_default_column_settings(self, *args, **kwargs):    
    if hasattr(self, "_cmdb_default_column_settings"):
      return self._cmdb_default_column_settings
    
    self._cmdb_default_column_settings = {
      "validation": lambda item: item["existing"] == item["new"]
    }
    return self._get_cmdb_default_column_settings()
  
  def _get_prefix_column(self, *args, **kwargs):    
    if hasattr(self, "_cmdb_prefix_columns"):
      return self._cmdb_prefix_columns

    self._cmdb_prefix_columns = [{
      "id": "source",
      "display": "Source",
      "handler": lambda item: self.get_cloud_client().get_provider(),
      "cmdb": self._get_cmdb_default_column_settings()
    },
    {
      "id": "cmdb_id",
      "display": "cmdbId",
      "handler": lambda item: self.get_common().helper_type().string().set_case(
        string_value= self.get_common().encryption().hash(hash_method= "sha1").generate_hash(
          data= self.get_common().helper_type().string().set_case(
            string_value= f'{self.get_cloud_client().get_provider()}-{item.get("raw_data").get("extra_id")}',
            case= "lower"
          ),
        ),
        case= "lower"
      ),
      "cmdb": self._get_cmdb_default_column_settings()
    }]
    
    return self._get_prefix_column(*args, **kwargs)
  
  def _get_postfix_column(self, *args, **kwargs):    
    if hasattr(self, "_cmdb_postfix_columns"):
      return self._cmdb_postfix_columns
    
    self._cmdb_postfix_columns = {}
    for data_container_key, settings in self._cmdb_postfix_column_settings.items():
      self._cmdb_postfix_columns[data_container_key] = []
      if settings.get("include_delete_column"):
        self._cmdb_postfix_columns[data_container_key].append({
          "id": "deleted",
          "display": "DELETED",
          "handler": lambda item: None,
          "cmdb": self._get_cmdb_default_column_settings()
        })
      if settings.get("include_empty_column"):
        self._cmdb_postfix_columns[data_container_key].append({
          "id": "empty",
          "display": "_",
          "handler": lambda item: None,
          "cmdb": self._get_cmdb_default_column_settings()
        })


    return self._get_postfix_column(*args, **kwargs)

  def __set_cmdb_postfix_columns(self, *args, **kwargs):
    
    self._cmdb_postfix_column_settings = {}

    for data_container_key, data_container_data in self.get_cmdb_data_containers().items():
      self._cmdb_postfix_column_settings[data_container_key] = self.get_common().helper_type().dictionary().merge_dictionary([
        {},
        {
          "include_delete_column": True,
          "include_empty_column": True,
        },
        data_container_data.get("cmdb_connector") if  data_container_data.get("cmdb_connector") is not None else {},
      ])
    

  def get_cmdb_name(self, *args, **kwargs):
    if hasattr(self, "_cmdb_name"):
      return self._cmdb_name
    
    self._cmdb_name = self.get_common().helper_type().string().set_case(
      string_value= self.get_cloud_share_config_value(config_key= "name"),
      case= "lower"
    )
    
    return self.get_cmdb_name(*args, **kwargs)
  
  def get_cloud_client(self, *args, **kwargs):
    return self.__cmdb_cloud_client
  
  def __set_cloud_client(self, auto_load = None, cloud_client = None, *args, **kwargs):
    if auto_load is not None:
      if auto_load.get_cloud_client() is not None:
        return self.__set_cloud_client(cloud_client= auto_load.get_cloud_client())

    self.__cmdb_cloud_client = cloud_client

  def get_cmdb_data_containers(self, *args, **kwargs):
    return self.__cmdb_data_containers
  
  def __set_cmdb_data_containers(self, auto_load = None, data_containers = None, *args, **kwargs):
    if auto_load is not None:
      if auto_load.get_cmdb_data_containers() is not None:
        return self.__set_cmdb_data_containers(data_containers= auto_load.get_cmdb_data_containers())
    
    self.__cmdb_data_containers = data_containers

  def get_cmdb_data_containers_column_names(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_columns_name"):
      return self._cmdb_data_containers_columns_name
    
    return None
  
  def _get_cmdb_data_containers_hidden(self, container, *args, **kwargs):
    if container.get("cmdb") is None:
      return (container.get("hidden") is True)
    
    if container.get("cmdb").get(self.get_cloud_share()) is not None:
      if container.get("cmdb").get(self.get_cloud_share()).get("hidden") is not None:
        return (container.get("cmdb").get(self.get_cloud_share()).get("hidden") is True)
      
    if container.get("cmdb").get("hidden") is not None:
      return (container.get("cmdb").get("hidden") is True)


    return False

  def _get_cmdb_data_containers_display(self, container, *args, **kwargs):
    if container.get("cmdb") is None:
      return (container.get("display"))
    
    if container.get("cmdb").get(self.get_cloud_share()) is not None:
      if "display" in container.get("cmdb").get(self.get_cloud_share()):
        return container.get("cmdb").get(self.get_cloud_share()).get("display")
      
    if "display" in container.get("cmdb"):
      return container.get("cmdb").get("display")


    return container.get("display")
  
  def _get_cmdb_data_containers_validation(self, container, *args, **kwargs):
    if container.get("cmdb") is None:
      return lambda item: item["existing"] == item["new"]
    
    if container.get("cmdb").get(self.get_cloud_share()) is not None:
      if "validation" in container.get("cmdb").get(self.get_cloud_share()):
        return container.get("cmdb").get(self.get_cloud_share()).get("validation")
      
    if "validation" in container.get("cmdb"):
      return container.get("cmdb").get("validation")


    return lambda item: item["existing"] == item["new"]


  def _set_cmdb_data_containers_column_names(self, container_name, columns, *args, **kwargs):    
    if not hasattr(self, "_cmdb_data_containers_columns_name"):
      self._cmdb_data_containers_columns_name = {}
    
    self._cmdb_data_containers_columns_name[container_name] = {}
    for column in columns:
  
      if self._get_cmdb_data_containers_hidden(container= column):
        continue
        
      self._cmdb_data_containers_columns_name[container_name][column["id"]] = {
        "display": self._get_cmdb_data_containers_display(container= column),
        "cmdb": self.get_common().helper_type().dictionary().merge_dictionary([
          {},
          column.get("cmdb") if column.get("cmdb") is not None else {},
          self._get_cmdb_default_column_settings()
        ])
      }

  def get_cmdb_data_containers_columns_raw_display_byid(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_columns_raw_display_byid"):
      return self._cmdb_data_containers_columns_raw_display_byid
    
    self._cmdb_data_containers_columns_raw_display_byid = {}
    for data_container in self._raw_cmdb_data_containers_columns.keys():
      self._cmdb_data_containers_columns_raw_display_byid[data_container] = {
       str(display):str(id) for id, display in self.get_cmdb_data_containers_columns_raw_byid_display()[data_container].items()
      }
    
    return self.get_cmdb_data_containers_columns_raw_display_byid()
  
  def get_cmdb_data_containers_columns_raw(self, *args, **kwargs):
    if hasattr(self, "_cmdb_raw_data_containers_columns"):
      return self._cmdb_raw_data_containers_columns
    
    self._cmdb_raw_data_containers_columns = {}
    for data_container in self._raw_cmdb_data_containers_columns.keys():
      self._cmdb_raw_data_containers_columns[data_container] = (
        self.get_common().helper_type().dictionary().merge_dictionary([
          {},
          {
            prefix.get("id"):prefix for prefix in self._get_prefix_column()
          },
          {
            id:column for id, column in self.get_cmdb_data_containers_column_names()[data_container].items()
          },
          {
            postfix.get("id"):postfix for postfix in self._get_postfix_column()[data_container]
          },
        ])
      )

    return self.get_cmdb_data_containers_columns_raw()
  
  def get_cmdb_data_containers_columns_raw_byid_display(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_columns_raw_byid_display"):
      return self._cmdb_data_containers_columns_raw_byid_display
    
    self._cmdb_data_containers_columns_raw_byid_display = {}
    for data_container in self._raw_cmdb_data_containers_columns.keys():
      self._cmdb_data_containers_columns_raw_byid_display[data_container] = {
        id:self._get_cmdb_data_containers_display(container= column) for id, column in self.get_cmdb_data_containers_columns_raw()[data_container].items()
      }
    
    return self.get_cmdb_data_containers_columns_raw_byid_display()

  
  def get_cmdb_data_containers_columns(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_columns"):
      return self._cmdb_data_containers_columns
    
    self._cmdb_data_containers_columns = {}
    for data_container in self._raw_cmdb_data_containers_columns.keys():
      self._cmdb_data_containers_columns[data_container] = list(self.get_cmdb_data_containers_columns_raw_byid_display()[data_container].values())
    
    return self.get_cmdb_data_containers_columns()
  
  def __set_cmdb_data_containers_columns(self, auto_load= None, container_columns= None, *args, **kwargs):
    if auto_load is not None:
      if auto_load.get_cmdb_data_containers() is not None:
        return self.__set_cmdb_data_containers_columns(container_columns= auto_load._raw_cmdb_data_containers_columns)

    self._raw_cmdb_data_containers_columns = container_columns
    for data_container, columns in self._raw_cmdb_data_containers_columns.items():
      self._set_cmdb_data_containers_column_names(container_name= data_container, columns= columns)
    
  def get_cmdb_data_containers_key_display(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_key_display"):
      return self._cmdb_data_containers_key_display
    
    self._cmdb_data_containers_key_display = {
      data_container_key:self._get_cmdb_data_containers_display(container= data_container) for data_container_key, data_container in self.get_cmdb_data_containers().items()
    }
    return self.get_cmdb_data_containers_key_display(*args, **kwargs)
  
  def get_cmdb_data_containers_display_key(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_display_key"):
      return self._cmdb_data_containers_display_key
    
    self._cmdb_data_containers_display_key = {
      data_container_display:data_container_key for data_container_key, data_container_display in self.get_cmdb_data_containers_key_display().items()
    }
    return self.get_cmdb_data_containers_display_key(*args, **kwargs)

  def get_report_data_column(self, container_key, report_data_item, column, *args, **kwargs):
    
    column_key = self.get_cmdb_data_containers_columns_raw_display_byid()[container_key].get(column)

    if column_key is None:
      return None
    
    return report_data_item.get(column_key)

  def save_data(self, report_data, *args, **kwargs):
    self._processed_report_data = {}
    for container_key, raw_data in report_data.items():
      self._processed_report_data[container_key] = []
      for data in raw_data:
        row_data = self.get_common().helper_type().dictionary().merge_dictionary([
          {},
          {prefix.get("id"):prefix.get("handler")(data) for prefix in self._get_prefix_column()},
          {postfix.get("id"):postfix.get("handler")(data) for postfix in self._get_postfix_column()[container_key]},
          data.get("data")
        ])
        self._processed_report_data[container_key].append(
          [self.get_report_data_column(container_key= container_key, report_data_item= row_data, column= column) for column in self.get_existing_columns_sorted_by_index()[container_key]]
        )
    
    self._sync_data(*args, **kwargs)

    
      