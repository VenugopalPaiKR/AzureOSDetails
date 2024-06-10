import time  
from azure.identity import DefaultAzureCredential  
from azure.mgmt.resource import SubscriptionClient, ResourceManagementClient  
from azure.mgmt.compute import ComputeManagementClient  
from azure.core.exceptions import HttpResponseError  
from openpyxl import Workbook  
  
# Initialize Azure credentials  
credential = DefaultAzureCredential()  
  
# Initialize the Excel workbook and sheet  
wb = Workbook()  
ws = wb.active  
ws.append(["Subscription Name", "Resource Group Name", "VM Name", "OS Name"])  
  
def get_running_vms(compute_client, resource_group_name):  
    vms = compute_client.virtual_machines.list(resource_group_name)  
    running_vms = []  
    for vm in vms:  
        print(vm.name)
        instance_view = compute_client.virtual_machines.instance_view(  
            resource_group_name=vm.id.split('/')[4],  
            vm_name=vm.name  
        )

        power_state = next((status.display_status for status in instance_view.statuses if status.code.startswith('PowerState/')), None)  
        if power_state == 'VM running':
            running_vms.append(vm)  

    return running_vms  

          
  
def main():  
    subscription_client = SubscriptionClient(credential)  
    for subscription in subscription_client.subscriptions.list():  
        subscription_name = subscription.display_name  
        print(f"Checking subscription: {subscription_name}")  
        compute_client = ComputeManagementClient(credential, subscription.subscription_id)  
        resource_client = ResourceManagementClient(credential, subscription.subscription_id)  
  
        for rg in resource_client.resource_groups.list():  
            resource_group_name = rg.name  
            print(f"Checking resource group: {resource_group_name}")  
            try:  
                running_vms = get_running_vms(compute_client, resource_group_name)  
                for vm in running_vms:  
                    vm_name = vm.name   
                    ws.append([subscription_name, resource_group_name, vm_name, 
                               vm.storage_profile.image_reference.offer if vm.storage_profile.image_reference else "Custom Image"])  
            except HttpResponseError as e:  
                if e.status_code == 429:  
                    print("API throttling occurred. Waiting before retrying...")  
                    time.sleep(30)  # Wait for 30 seconds before retrying  
                else:  
                    print(f"An error occurred: {e.message}")  
        print(f"Finished checking subscription: {subscription_name}")  
  
    wb.save("azure_vms_os_info.xlsx")  
    print("Excel file created: azure_vms_os_info.xlsx")  
  
if __name__ == "__main__":  
    main()  
