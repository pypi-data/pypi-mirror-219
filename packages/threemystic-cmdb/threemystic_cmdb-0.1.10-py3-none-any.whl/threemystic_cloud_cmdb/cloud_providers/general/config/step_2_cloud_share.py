from threemystic_cloud_cmdb.cloud_providers.general.config.base_class.base import cloud_cmdb_general_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers

import time

class cloud_cmdb_general_config_step_2_cloud_share(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_general_config_step_2_cloud_share", *args, **kwargs)
    

  def step(self, cloud_share= None, *args, **kwargs):
    if not super().step(run_base_config= True):
      return
    
    if self.get_common().helper_type().string().is_null_or_whitespace(string_value= cloud_share):
      return
    
    if cloud_share == "ms365":
      self._step_ms365_tenant(cloud_share= cloud_share)
      return
  
  def get_tenant_id_index(self, data_client, cloud_share):
    try:
      index = 1
      for tenant in data_client.get_cloud_client().get_tenants():
        if data_client.get_cloud_client().get_tenant_id(tenant= tenant) == self.get_cloud_share_config_value(config_key= cloud_share).get('tenant_id'):
          return index
        index += 1
    except:
      pass

    return None
    
  def _step_ms365_tenant(self, cloud_share, *args, **kwargs):
    from threemystic_cloud_data_client.cloud_data_client import cloud_data_client
    data_client = cloud_data_client(
      provider= "azure",
      logger= self.get_logger(), 
      common= self.get_common()      
    ).client(suppress_parser_help= True)

    
    print("-----------------------------")
    print()
    print("What tenant will store the cmdb data?")
    print()
    print("-----------------------------")
    
    
    index = 1
    print("loading tenants")
    data_client.get_cloud_client().get_tenants()
    print(f"0: Remove Entry")
    for tenant in data_client.get_cloud_client().get_tenants():
      print(f"{index}: {data_client.get_cloud_client().get_tenant_id(tenant= tenant)}")
      index += 1

    tenant_index = self.get_tenant_id_index(data_client= data_client, cloud_share= cloud_share)
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "tenant_id": {
          "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) and self.get_common().helper_type().general().is_integer(item) and self.get_common().helper_type().int().get(item) >= 0 and self.get_common().helper_type().int().get(item) <= len(data_client.get_cloud_client().get_tenants()),
          "messages":{
            "validation": f"Valid options are: 0 - {len(data_client.get_cloud_client().get_tenants())}",
          },
          "conversion": lambda item: self.get_common().helper_type().int().get(item) if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) else item,
          "desc": f"Please select the tenant to use \nValid Options: 0 - {len(data_client.get_cloud_client().get_tenants())}",
          "default": tenant_index,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": tenant_index is not None
        },
      }
    )

    if(response is not None):
      if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= response.get("tenant_id").get("formated")):
        self.get_cloud_share_config_value(
          config_key= cloud_share
        )["tenant_id"] = data_client.get_cloud_client().get_tenant_id(tenant= data_client.get_cloud_client().get_tenants()[response.get("tenant_id").get("formated") - 1]) if response.get("tenant_id").get("formated") > 0 else ""
        self._save_config_cloud_share()

        print("-----------------------------")
        print()
        print(f"Tenant ID Updated: {self.get_cloud_share_config_value(config_key= cloud_share).get('tenant_id')}")
        print()
        print("-----------------------------")

        self._step_ms365_tenant_location(cloud_share= cloud_share, data_client= data_client)
        return
      
    
    print("-----------------------------")
    print()
    print(f"Tenant ID NOT Updated")
    print()
    print("-----------------------------")

  
  def get_group_index(self, group_options, cloud_share):
    try:
      index = 0
      for group in group_options:
        if group.get("id") == self.get_cloud_share_config_value(config_key= cloud_share).get('group'):
          return index
        index += 1
    except:
      pass

    return None
  
  def _step_ms365_tenant_location(self, cloud_share, data_client, ms_graph = None, *args, **kwargs):

    print("-----------------------------")
    print()
    print("Where drive/group will the CMDB be stored in")
    print()
    print("-----------------------------")
    
    
    index = 1
    print("loading groups")
    group_options = [
      {
        "id": "Remove Entry"
      },      
      {
        "id": "me"
      }
    ]

    if ms_graph is None:
      ms_graph = self.get_common().graph().graph(graph_method= "msgraph", credentials= data_client.get_cloud_client().get_tenant_credential(tenant= self.get_cloud_share_config_value(config_key= cloud_share).get('tenant_id')))
    user_groups = ms_graph.send_request(
      url = ms_graph.generate_graph_url(resource= "me", base_path= "/transitiveMemberOf/microsoft.graph.group")
    )
    
    group_options = group_options + [
      {"id": group.get("id"), "display": f"{group.get('id')} - {group.get('displayName')}"} for group in user_groups.get("value")
    ]
    index = 0
    for option in group_options:
      if option.get("display") is not None:
        print(f'{index}: {option.get("display")}')
        index += 1    
        continue
      
      print(f'{index}: {option.get("id")}')
      index += 1    

    group_index = self.get_group_index(group_options= group_options, cloud_share= cloud_share)
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "group": {
          "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) and self.get_common().helper_type().general().is_integer(item) and self.get_common().helper_type().int().get(item) >= 0 and self.get_common().helper_type().int().get(item) <= (len(group_options) - 1),
          "messages":{
            "validation": f"Valid options are: 0 - {len(group_options) - 1}",
          },
          "conversion": lambda item: self.get_common().helper_type().int().get(item),
          "desc": f"Please select the tenant to use \nValid Options: 0 - {len(group_options) - 1}",
          "default": group_index,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": group_index is not None
        },
      }
    )

    if(response is not None):
      if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= response.get("group").get("formated")):
        self.get_cloud_share_config_value(
          config_key= cloud_share
        )["group"] = group_options[response.get("group").get("formated")].get("id") if response.get("group").get("formated") > 0 else ""
        self._save_config_cloud_share()

        print("-----------------------------")
        print()
        print(f"Group Updated: {self.get_cloud_share_config_value(config_key= cloud_share).get('group')}")
        print()
        print("-----------------------------")

        self._step_ms365_tenant_path(cloud_share= cloud_share, data_client= data_client, ms_graph= ms_graph)
        return
      
    
    print("-----------------------------")
    print()
    print(f"Group NOT Updated")
    print()
    print("-----------------------------")

  

  
  def get_drive_item_index(self, drive_item_ids, existing_drive_item_ids, drive_item_id_options, position, cloud_share):
    try:
      index = 0
      drive_id = None
      drive_item_ids_position = position + 1
      if drive_item_ids[-1]["id"] != existing_drive_item_ids[position]["id"]:
        return None
      
      
      if len(existing_drive_item_ids) > drive_item_ids_position:
        if self.get_common().helper_type().general().is_type(obj= existing_drive_item_ids[drive_item_ids_position], type_check= dict):
          drive_id = existing_drive_item_ids[drive_item_ids_position]
      
      if drive_id is None:
        return None
      
      if drive_id.get("id") is None:
        return None
      
      for drive_item in drive_item_id_options[position]:
        if (self.get_common().helper_type().string().set_case(string_value= drive_item.get("id"), case= "lower") == 
            self.get_common().helper_type().string().set_case(string_value= drive_id.get("id"), case= "lower")):
          return index
        index += 1
    except:
      pass

    return None
  
  def generate_new_grive_item_folder(self, ms_graph, ms_graph_resource, ms_graph_resource_id, drive_item_parent_id, drive_item_id_options):
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "name": {
          "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) and self.get_common().helper_path().is_valid_filename(file_name= item),
          "messages":{
            "validation": f"Valid options are: {self.get_supported_cloud_share()}",
          },
          "conversion": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower"),
          "desc": f"What is the name of the folder you would like to create? (blank will cancel)",
          "default": None,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": True
        },
      }
    )

    if response is None:
      print("canceled")
      time.sleep(2)
      return None
    
    if response.get("name") is None:
      print("canceled")
      time.sleep(2)
      return None
    
    if response.get("name").get("formated") is None:
      print("canceled")
      time.sleep(2)
      return None
    
    try:
      for drive_option in drive_item_id_options:
        if (self.get_common().helper_type().string().set_case(string_value= drive_option.get("name"), case= "lower") == 
            self.get_common().helper_type().string().set_case(string_value= response.get("name").get("formated"), case= "lower")):
          return drive_option

      file_data = ms_graph.send_request(
        url = ms_graph.generate_graph_url(resource= ms_graph_resource, resource_id= ms_graph_resource_id, base_path= f'drive/items/{drive_item_parent_id}/children'),
        data = ms_graph.create_folder_data(
          name = response.get("name").get("formated"),
          folder_args = {"@microsoft.graph.conflictBehavior": "fail"}
        ),      
        method="post"
      )
      return {"id": file_data["id"], "name": file_data.get('name'), "display": f"{file_data.get('id')} - {file_data.get('name')}"}
    except Exception as err:
      print("Could not create that folder")
      print(err)
      time.sleep(3)
      return None
    
  def get_drive_item_location_options(self, ms_graph,ms_graph_resource, ms_graph_resource_id, drive_item_id, cloud_share):
    location_options_base = [
      {
      "id": "refresh",
      "display": "Refresh List"
    }
    ]
    parent_folder = {
      "id": "parent_folder",
      "display": "Parent Folder"
    }
      
    new_folder = {
      "id": "new_folder",
      "display": "New Folder"
    }
      
    select = {
      "id": "select_folder",
      "display": "Select"
    }

    if self.get_cloud_share_config_value(config_key= cloud_share).get('group') == "me" or drive_item_id != "root":
      location_options_base.append(select)
      location_options_base.append(parent_folder)
      location_options_base.append(new_folder)
      
    

    base_path = f"{drive_item_id}" if self.get_cloud_share_config_value(config_key= cloud_share).get('group') == "me" else f"items/{drive_item_id}"
    
    local_drive_options = ms_graph.send_request(
      url = ms_graph.generate_graph_url(resource= ms_graph_resource, resource_id= ms_graph_resource_id, base_path= f"drive/{base_path}/children")
    )

    return location_options_base + [
      {"id": drive_option.get("id"), "name": drive_option.get('name'), "display": f"{drive_option.get('id')} - {drive_option.get('name')}"} for drive_option in local_drive_options.get("value") if drive_option.get("file") is None and drive_option.get("folder") is not None
    ]
  
  def _step_ms365_tenant_path(self, cloud_share, data_client, ms_graph, *args, **kwargs):

    print("-----------------------------")
    print()
    print("What folder will the CMDB be stored in")
    print("If you have moved the folder where the cmdb is stored you could break the hierarchy used to validate the path, but the upload should be fine.")
    print("This is because the upload does not look at the pat, IE. /3mystic/data/cmdb, it looks at the last drive ID and uses that which shouldn't change as you move folders.")
    print()
    print("-----------------------------")
    
    
    index = 1
    print("loading folders")

    
    existing_drive_item_ids = self.get_cloud_share_config_value(config_key= cloud_share).get('drive_id')
    drive_item_ids = [
      {"id": "root", "display": "root"}
    ]
    
    if not self.get_common().helper_type().general().is_type(obj= drive_item_ids, type_check= list):
      existing_drive_item_ids = [
        {"id": "root", "display": "root"}
      ]
    try:
      if len(existing_drive_item_ids) < 1:
        existing_drive_item_ids.append({"id": "root", "display": "root"})
      if not self.get_common().helper_type().general().is_type(obj= drive_item_ids[0], type_check= dict):
        existing_drive_item_ids[0] = ({"id": "root", "display": "root"})
    except:
      existing_drive_item_ids = [
        {"id": "root", "display": "root"}
      ]

    drive_item_position = 0
    drive_item_id_options = []
    drive_id_selected = False
    main_graph_resource = "me" if self.get_cloud_share_config_value(config_key= cloud_share).get('group') == "me" else f"groups"
    main_graph_resource_id = self.get_cloud_share_config_value(config_key= cloud_share).get('group') if self.get_cloud_share_config_value(config_key= cloud_share).get('group') != "me" else None
    while not drive_id_selected:
      
      try:
        drive_item_id_options.append(self.get_drive_item_location_options(ms_graph= ms_graph, ms_graph_resource= main_graph_resource, ms_graph_resource_id= main_graph_resource_id, cloud_share= cloud_share, drive_item_id= drive_item_ids[drive_item_position]['id']))
      except Exception as err:
        print("Could not get list of folders")
        print(err)
        if main_graph_resource == "me":
          print("possible issue is you are trying to store your onedrive space. please switch to one of the group drives")
          self._step_ms365_tenant_location(cloud_share= cloud_share, data_client= data_client, ms_graph= ms_graph)
          time.sleep(3)
        return

      print("-----------------------------")
      print(f"Folders in {drive_item_ids[drive_item_position].get('display')}")
      print("-----------------------------")
      
      drive_item_index = self.get_drive_item_index(drive_item_ids= drive_item_ids, existing_drive_item_ids= existing_drive_item_ids, drive_item_id_options= drive_item_id_options, position= drive_item_position, cloud_share= cloud_share,)
      
      index = 0
      for option in drive_item_id_options[drive_item_position]:
        print(f'{index}: {option.get("display")}')
        if drive_item_position > 0 and drive_item_index is None and option.get("id") == "select_folder":
          drive_item_index = index
        index += 1 

      response = self.get_common().generate_data().generate(
        generate_data_config = {
          "drive_id": {
            "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) and self.get_common().helper_type().general().is_integer(item) and self.get_common().helper_type().int().get(item) >= 0 and self.get_common().helper_type().int().get(item) <= (len(drive_item_id_options[drive_item_position]) - 1),
            "messages":{
              "validation": f"Valid options are: 0 - {len(drive_item_id_options[drive_item_position]) - 1}",
            },
            "conversion": lambda item: self.get_common().helper_type().int().get(item) if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) else None,
            "desc": f"Please select the tenant to use \nValid Options: 0 - {len(drive_item_id_options[drive_item_position]) - 1}",
            "default": drive_item_index,
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": drive_item_index
          },
        }
      )

      if response is None:
        print("-----------------------------")
        print()
        print(f"Drive ID NOT Updated")
        print()
        print("-----------------------------")
        return
      
      drive_id_option = drive_item_id_options[drive_item_position][response.get("drive_id").get("formated")]
      if drive_id_option["id"] == "refresh":
        drive_item_id_options.pop()
        continue

      if drive_id_option["id"] == "select_folder":
        drive_id_selected = True
        continue
      
      if drive_id_option["id"] == "new_folder":
        new_folder_info = self.generate_new_grive_item_folder(
          ms_graph= ms_graph,
          ms_graph_resource= main_graph_resource,
          ms_graph_resource_id= main_graph_resource_id,
          drive_item_parent_id= drive_item_ids[drive_item_position].get("id"),
          drive_item_id_options = drive_item_id_options[drive_item_position]
        )
        if new_folder_info is None:
          continue

        drive_item_ids.append(new_folder_info)
        drive_item_position = drive_item_position + 1
        continue
      
      if drive_id_option["id"] == "parent_folder":
        if len(drive_item_id_options) > 1:
          drive_item_ids.pop()
          drive_item_id_options.pop()
          drive_item_id_options.pop()
          drive_item_position = drive_item_position - 1
          continue
        print("already at the root")
        continue
      
      
      drive_item_ids.append(drive_id_option)
      drive_item_position = drive_item_position + 1
      
      
    self.get_cloud_share_config_value(
      config_key= cloud_share
    )["drive_id"] = drive_item_ids
    self._save_config_cloud_share()
    
    print("-----------------------------")
    print()
    print(f"Drive ID Updated: {drive_item_ids[-1]}")
    print()
    print("-----------------------------")

    from threemystic_cloud_cmdb.cloud_providers.general.config.step_3 import cloud_cmdb_general_config_step_3 as step
    next_step = step(common= self.get_common(), logger= self.get_logger())
    
    if not self.is_general_config_completed_only():
      self.update_general_config_completed(status= "CloudShare")

    next_step.step(cloud_share= self.get_cloud_share_config_value(config_key= "type"))

    
  
    
  
