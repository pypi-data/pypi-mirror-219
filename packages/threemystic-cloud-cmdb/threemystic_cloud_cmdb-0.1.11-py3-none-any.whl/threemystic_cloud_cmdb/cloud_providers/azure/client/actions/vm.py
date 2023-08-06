from threemystic_cloud_cmdb.cloud_providers.azure.client.actions.base_class.base import cloud_cmdb_azure_client_action_base as base
import asyncio
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


class cloud_cmdb_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="vm", 
      logger_name= "cloud_cmdb_azure_client_action_vm", 
      uniqueid_lambda = lambda: True
      *args, **kwargs)
    
  
  def _load_cmdb_general_data(self, *args, **kwargs):
    if hasattr(self, "_cmdb_general_data_loaded"):
      return self._cmdb_general_data_loaded
    
    self._cmdb_general_data_loaded = {
      "vmss":{
        "display":"VMSS_ASG",
      },
      self.get_cmdb_data_action():{
        "display":"VM_LongLived",
      }
    }
    return self._load_cmdb_general_data()
  
  def _load_cmdb_column_data(self, *args, **kwargs):
    if hasattr(self, "_cmdb_column_data_loaded"):
      return self._cmdb_column_data_loaded
    
    self._cmdb_column_data_loaded = {      
      "vmss": {
        "AutoScalingGroup":{
          "display": "AutoScalingGroup",
          "handler": lambda item: "VMSS"
        },        
        "ASGArn": {
          "display": "ID",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="extra_id"),
          "cmdb": {
            "display": "ID_Arn"
          }
        },
        "ASGName": {
          "display": "Name",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="name")
        },
        "ASGMin": {
          "display": "Min",
          "handler": lambda item: None
        },
        "ASGDesiredCapacity": {
          "display": "Desired",
          "handler": lambda item: None
        },
        "ASGMaxSize": {
          "display": "Max",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["sku", "capacity"])
        },
        "ASGEffective": {
          "display": "Effective",
          "handler": lambda item: None
        },
        "InstanceType": {
          "display": "Instance Type",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["sku", "name"])
        },
        "AMIID": {
          "display": "AMI ID",
          "handler": lambda item: (self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","id"]) 
                                   if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","id"])) else 
                                   self.get_common().helper_type().string().join(separator= ".", str_array= [self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","publisher"]), self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","sku"])])
          )
        },
        "AMIName": {
          "display": "AMI Name",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ".", str_array= [self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","publisher"]), self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","sku"]), self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","version"])])  
        },
        "AMIDescription": {
          "display": "AMI Description",
          "handler": lambda item: None
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: self.generate_resource_tags_csv(tags= self.get_item_data_value(item_data= item, value_key=["tags"]))
        },
      },
      self.get_cmdb_data_action(): {
        "EC2":{
          "display": "Type",
          "handler": lambda item: "VM"
        },
        "InstanceID":{
          "display": "Instance ID",
          "handler": lambda item: self.get_cloud_client().get_resource_id_from_resource(
              resource= self.get_item_data_value(item_data= item, value_key="extra_id"))
        },
        "InstanceType":{
          "display": "Instance Type",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["properties","hardwareProfile","vmSize"])
        },
        "Platform":{
          "display": "Platform",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","osDisk","osType"])
        },
        "PlatformName":{
          "display": "Platform Name",
          "handler": lambda item: None
        },
        "PlatformVersion":{
          "display": "Platform Version",
          "handler": lambda item: None
        },
        "IAMRole":{
            "display": "IAM Role",
            "handler": lambda item: None
        },
        "SSMPingStatus":{
          "display": "SSM Ping Status",
          "handler": lambda item: None
        },
        "SSMLastPingTime":{
          "display": "SSM Last Ping Time",
          "handler": lambda item: None
        },
        "SSMVersion":{
          "display": "SSM Version",
          "handler": lambda item: None
        },
        "AMIID": {
          "display": "AMI ID",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ".", str_array= [self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","publisher"]), self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","sku"])]) 
        },
        "AMIName": {
          "display": "AMI Name",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ".", str_array= [self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","publisher"]), self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","sku"]), self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","version"])])
        },
        "AMIDescription": {
          "display": "AMI Description",
          "handler": lambda item: None
        },
        "LaunchTime":{
          "display": "LaunchTime",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["extra_resource","createdTime"])
        }, 
        "Monitoring":{
          "display": "Monitoring",
          "handler": lambda item: None
        },
        "Tenancy":{
          "display": "Tenancy",
          "handler": lambda item: None
        },
        "PrivateDnsName":{
          "display": "PrivateDnsName",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_private_fqdn(vm= item, vm_nics= self.get_item_data_value(item_data= item, value_key=["extra_nics"])))
        },
        "PrivateIpAddress":{
          "display": "PrivateIpAddress",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_private_ips(vm= item, vm_nics= self.get_item_data_value(item_data= item, value_key=["extra_nics"])))
        },
        "ProductCodes":{
          "display": "ProductCodes",
          "handler": lambda item: None
        },
        "PublicDnsName":{
          "display": "PublicDnsName",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_public_ips_fqdn_nics(vm= item, vm_nics= self.get_item_data_value(item_data= item, value_key=["extra_nics"])))
        },
        "SubnetId":{
          "display": "SubnetId",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_subnets(vm= item, vm_nics= self.get_item_data_value(item_data= item, value_key=["extra_nics"])))
        },
        "VpcId":{
          "display": "VpcId",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_vnets(vm= item, vm_nics= self.get_item_data_value(item_data= item, value_key=["extra_nics"])))
        },
        "Architecture":{
          "display": "Architecture",
          "handler": lambda item: None
        },
        "EbsOptimized":{
          "display": "EbsOptimized",
          "handler": lambda item: None
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: self.generate_resource_tags_csv(tags= self.get_item_data_value(item_data= item, value_key=["tags"]))
        },
        "VirtualizationType":{
          "display": "VirtualizationType",
          "handler": lambda item: None
        },
        "AvailabilitySet":{
          "display": "AvailabilitySet",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["extra_availability_set", "name"])
        },
        "LBType":{
          "display": "LB Type",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= "-", 
            str_array= self._get_vm_load_balancers_type(vm_load_balancers= self.get_item_data_value(item_data= item, value_key=["extra_load_balancers"])))
        },
        "LBDNSName":{
          "display": "LB DNS Name",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_public_ips_fqdn_load_balancers(vm= item, vm_load_balancers= self.get_item_data_value(item_data= item, value_key=["extra_load_balancers"])))
        },
        "LBName":{
          "display": "LB Name",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= "-", 
            str_array= self._get_vm_load_balancers_name(vm_load_balancers= self.get_item_data_value(item_data= item, value_key=["extra_load_balancers"])))
        },
      } 
    }
    return self._load_cmdb_column_data()
  
  
  def _get_vm_load_balancers_name(self, vm_load_balancers, *args, **kwargs):

    if vm_load_balancers is None:
      return []

    return [
      self.get_item_data_value(item_data= load_balancer, value_key=["load_balancer", "name"])
      for load_balancer in vm_load_balancers
      if self.get_item_data_value(item_data= load_balancer, value_key=["load_balancer", "name"]) is not None
    ]
  
  
  def _get_vm_load_balancers_type(self, vm_load_balancers, *args, **kwargs):

    if vm_load_balancers is None:
      return []

    return [
      self.get_item_data_value(item_data= load_balancer, value_key=["load_balancer", "sku", "name"])
      for load_balancer in vm_load_balancers
      if self.get_item_data_value(item_data= load_balancer, value_key=["load_balancer", "sku", "name"]) is not None
    ]

  def _get_vm_vnets(self, vm, vm_nics, *args, **kwargs):
    subnets = self._get_vm_subnets(vm= vm, vm_nics= vm_nics)

    if subnets is None:
      return []
    
    vnet_ids = []
    for subnet in subnets:
      subnet_lower = self.get_common().helper_type().string().set_case(string_value= subnet, case= "lower")
      vnet_ids.append(subnet_lower[0:subnet_lower.rfind("/subnets/")])
    
    return vnet_ids
  
  def _get_vm_subnets(self, vm, vm_nics, *args, **kwargs):
    if hasattr(self, "_vm_subnets"):
      if self.get_cloud_client().get_resource_id_from_resource(resource= vm) in self._vm_subnets:
        return self._vm_subnets[self.get_cloud_client().get_resource_id_from_resource(resource= vm)]

    if not hasattr(self, "_vm_subnets"):
      self._vm_subnets = {}

    if vm_nics is None:
      self._vm_subnets[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
      return self._get_vm_subnets(vm= vm, vm_nics= vm_nics, *args, **kwargs)
    
    self._vm_subnets[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = [
      self.get_cloud_client().get_resource_id_from_resource(resource= self.get_item_data_value(item_data= ip_config, value_key=["properties","subnet"]))
      for ip_config in self._get_vm_nic_ip_configurations(vm= vm, vm_nics= vm_nics)
      if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= self.get_cloud_client().get_resource_id_from_resource(resource= self.get_item_data_value(item_data= ip_config, value_key=["properties","subnet"])) )
    ]
        
    return self._get_vm_subnets(vm= vm, vm_nics= vm_nics)
  
  def _get_vm_private_fqdn(self, vm, vm_nics, *args, **kwargs):    
    if hasattr(self, "_vm_nic_fqdn"):
      if self.get_cloud_client().get_resource_id_from_resource(resource= vm) in self._vm_nic_fqdn:
        return self._vm_nic_fqdn[self.get_cloud_client().get_resource_id_from_resource(resource= vm)]

    if not hasattr(self, "_vm_nic_fqdn"):
      self._vm_nic_fqdn = {}

    if vm_nics is None:
      self._vm_nic_fqdn[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
      return self._get_vm_private_fqdn(vm= vm, vm_nics= vm_nics, *args, **kwargs)
    
    self._vm_nic_fqdn[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
    for nic in vm_nics:
      dns_settings = self.get_item_data_value(item_data= nic, value_key=["properties","dnsSettings"])
      if self.get_item_data_value(item_data= dns_settings, value_key=["internalDomainNameSuffix"]) is None:
        continue
      
      self._vm_nic_fqdn[self.get_cloud_client().get_resource_id_from_resource(resource= vm)].append(self.get_item_data_value(item_data= dns_settings, value_key=["internalDomainNameSuffix"]))

    
    return self._get_vm_private_fqdn(vm= vm, vm_nics= vm_nics, *args, **kwargs)
  
  def _get_vm_public_ips_ip(self, vm_nics, vm_load_balancers, *args, **kwargs):
    return [
      public_ip.ip_address
      for public_ip in self._get_vm_public_ips(vm= vm, vm_nics= vm_nics, vm_load_balancers= vm_load_balancers)
    ]   
    
  def _get_vm_private_ips(self, vm, vm_nics, *args, **kwargs):

    if vm_nics is None:
      return []

    return [
      self.get_item_data_value(item_data= ip_config, value_key=["properties","privateIPAddress"])
      for ip_config in self._get_vm_nic_ip_configurations(vm= vm, vm_nics= vm_nics)
      if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= self.get_item_data_value(item_data= ip_config, value_key=["properties","privateIPAddress"]) )
    ]
  
  def _get_vm_nic_ip_configurations(self, vm, vm_nics, *args, **kwargs):    
    if hasattr(self, "_vm_nic_ip_configurations"):
      if self.get_cloud_client().get_resource_id_from_resource(resource= vm) in self._vm_nic_ip_configurations:
        return self._vm_nic_ip_configurations[self.get_cloud_client().get_resource_id_from_resource(resource= vm)]

    if not hasattr(self, "_vm_nic_ip_configurations"):
      self._vm_nic_ip_configurations = {}

    if vm_nics is None:
      self._vm_nic_ip_configurations[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
      return self._get_vm_nic_ip_configurations(vm= vm, vm_nics= vm_nics, *args, **kwargs)
    
    self._vm_nic_ip_configurations[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
    for nic in vm_nics:
      ip_configurations = self.get_item_data_value(item_data= nic, value_key=["properties","ipConfigurations"])
      if ip_configurations is None:
        continue
      
      self._vm_nic_ip_configurations[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] += [ip_config for ip_config in ip_configurations]

    
    return self._get_vm_nic_ip_configurations(vm= vm, vm_nics= vm_nics, *args, **kwargs)
    
  
  def _get_vm_public_ips_fqdn_load_balancers(self, vm, vm_load_balancers, *args, **kwargs):
    public_fqdn = []
    for public_ip in self._get_vm_public_ips_vm_load_balancers(vm= vm, vm_load_balancers= vm_load_balancers):
      if self.get_item_data_value(item_data= public_ip, value_key=["properties","dnsSettings", "fqdn"]) is None:
        if self.get_item_data_value(item_data= public_ip, value_key=["properties","ipAddress"]) is not None:
          public_fqdn.append(self.get_item_data_value(item_data= public_ip, value_key=["properties","ipAddress"]))

        continue
      public_fqdn.append(self.get_item_data_value(item_data= public_ip, value_key=["properties","dnsSettings", "fqdn"]))
    
    return public_fqdn
  
  def _get_vm_public_ips_fqdn_nics(self, vm, vm_nics, *args, **kwargs):
    public_fqdn = []
    for public_ip in self._get_vm_public_ips_vm_nics(vm= vm, vm_nics= vm_nics):
      if self.get_item_data_value(item_data= public_ip, value_key=["properties","dnsSettings", "fqdn"]) is None:
        if self.get_item_data_value(item_data= public_ip, value_key=["properties","ipAddress"]) is not None:
          public_fqdn.append(self.get_item_data_value(item_data= public_ip, value_key=["properties","ipAddress"]))

        continue
      public_fqdn.append(self.get_item_data_value(item_data= public_ip, value_key=["properties","dnsSettings", "fqdn"]))
    
    return public_fqdn

  def _get_vm_public_ips_ip(self, vm_nics, vm_load_balancers, *args, **kwargs):
    public_ips = []
    for public_ip in self._get_vm_public_ips(vm= vm, vm_nics= vm_nics, vm_load_balancers= vm_load_balancers):
      if self.get_item_data_value(item_data= public_ip, value_key=["properties","ipAddress"]) is None:
        continue

      public_ips.append(self.get_item_data_value(item_data= public_ip, value_key=["properties","ipAddress"]))    

    return public_ips

  
  def _get_vm_public_ips_vm_load_balancers(self, vm, vm_load_balancers, *args, **kwargs):
    if hasattr(self, "_vm_load_balancers"):
      if self.get_cloud_client().get_resource_id_from_resource(resource= vm) in self._vm_load_balancers:
        return self._vm_load_balancers[self.get_cloud_client().get_resource_id_from_resource(resource= vm)]

    if not hasattr(self, "_vm_load_balancers"):
      self._vm_load_balancers = {}

    if vm_load_balancers is None:
      self._vm_load_balancers[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
      return self._get_vm_public_ips_vm_load_balancers(vm= vm, vm_load_balancers= vm_load_balancers, *args, **kwargs)

    self._vm_load_balancers[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
    for load_balancer in vm_load_balancers:
      if self.get_item_data_value(item_data= load_balancer, value_key=["extra_public_ips"]) is None:
        continue

      for ip in self.get_item_data_value(item_data= load_balancer, value_key=["extra_public_ips"]):
        self._vm_load_balancers[self.get_cloud_client().get_resource_id_from_resource(resource= vm)].append(ip)

    return self._get_vm_public_ips_vm_load_balancers(vm= vm, vm_load_balancers= vm_load_balancers, *args, **kwargs)

  
  def _get_vm_public_ips_vm_nics(self, vm, vm_nics, *args, **kwargs):
    if hasattr(self, "_vm_nic_public_ips"):
      if self.get_cloud_client().get_resource_id_from_resource(resource= vm) in self._vm_nic_public_ips:
        return self._vm_nic_public_ips[self.get_cloud_client().get_resource_id_from_resource(resource= vm)]

    if not hasattr(self, "_vm_nic_public_ips"):
      self._vm_nic_public_ips = {}

    if vm_nics is None:
      self._vm_nic_public_ips[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
      return self._get_vm_public_ips_vm_nics(vm= vm, vm_nics= vm_nics, *args, **kwargs)

    self._vm_nic_public_ips[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
    for nic in vm_nics:
      if self.get_item_data_value(item_data= nic, value_key=["extra_public_ips"]) is None:
        continue

      for ip in self.get_item_data_value(item_data= nic, value_key=["extra_public_ips"]):
        self._vm_nic_public_ips[self.get_cloud_client().get_resource_id_from_resource(resource= vm)].append(ip)

    return self._get_vm_public_ips_vm_nics(vm= vm, vm_nics= vm_nics, *args, **kwargs)

  def _get_vm_public_ips(self, vm, vm_nics, vm_load_balancers, *args, **kwargs):
    if hasattr(self, "_vm_public_ips"):
      if self.get_cloud_client().get_resource_id_from_resource(resource= vm) in self._vm_public_ips:
        return self._vm_public_ips[self.get_cloud_client().get_resource_id_from_resource(resource= vm)]

    if not hasattr(self, "_vm_public_ips"):
      self._vm_public_ips = {}

    if vm_nics is None and vm_load_balancers is None:
       self._vm_public_ips[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = []
       return self._get_vm_public_ips(vm= vm, vm_nics= vm_nics, vm_load_balancers= vm_load_balancers, *args, **kwargs)

    self._vm_public_ips[self.get_cloud_client().get_resource_id_from_resource(resource= vm)] = (
      self._get_vm_public_ips_vm_nics(vm= vm, vm_nics= vm_nics) +
      self._get_vm_public_ips_vm_load_balancers(vm= vm, vm_load_balancers= vm_load_balancers)
    )     
    
    return self._get_vm_public_ips(vm= vm, vm_nics= vm_nics, vm_load_balancers= vm_load_balancers, *args, **kwargs)
