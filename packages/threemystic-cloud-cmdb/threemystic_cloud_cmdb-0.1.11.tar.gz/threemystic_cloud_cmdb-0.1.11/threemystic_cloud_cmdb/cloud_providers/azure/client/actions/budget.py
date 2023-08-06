from threemystic_cloud_cmdb.cloud_providers.azure.client.actions.base_class.base import cloud_cmdb_azure_client_action_base as base
import asyncio
from decimal import Decimal, ROUND_HALF_UP
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import GranularityType,ForecastDefinition,ForecastType,ForecastTimeframe,ForecastTimePeriod,QueryDefinition,TimeframeType,ExportType,QueryTimePeriod


class cloud_cmdb_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="budget", 
      logger_name= "cloud_cmdb_azure_client_action_budget", 
      uniqueid_lambda = lambda: True
      *args, **kwargs)
  
  def _load_cmdb_general_data(self, *args, **kwargs):
    if hasattr(self, "_cmdb_general_data_loaded"):
      return self._cmdb_general_data_loaded
    
    self._cmdb_general_data_loaded = {
      self.get_cmdb_data_action():{
        "display":"Budget",
        "include_region": False,
        "include_resourcegroup": False,
        "include_requiredtags": False,
        "cmdb_connector": {
          "include_delete_column": False
        }
        
      }
    }
    return self._load_cmdb_general_data()
  
  def _load_cmdb_column_data(self, *args, **kwargs):
    if hasattr(self, "_cmdb_column_data_loaded"):
      return self._cmdb_column_data_loaded
    
    self._cmdb_column_data_loaded = {
      self.get_cmdb_data_action(): {
        "last_run":{
          "display": "LastRun",
          "handler": lambda item: self.get_common().helper_type().datetime().remove_tzinfo(dt= self.get_data_start()),
          "cmdb": {
              "handler": lambda item: self.get_data_start(),
          }
        },
        "last_seven_days":{
          "display": "Last7Days",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="last_seven_days")
        },
        "month_to_date":{
          "display": "MonthToDate",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="month_to_date")
        },
        "month_forecast":{
          "display": "MonthTotalForcast",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="month_forecast")
        },
        "year_to_date":{
          "display": "FiscalYearToDate",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="fiscal_year_to_date")
        },
        "year_forecast":{
          "display": "FiscalYearForcast",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="fiscal_year_forecast")
        },
      } 
    }
    return self._load_cmdb_column_data()
 