# Retrieve OS details for Azure VMs
This script is used to retrieve the installed OS details for running VMs across all the resource groups in Azure subscriptions. The output is stored in an excel file

## Steps to run the script
1. Login to your Azure account
2. Connect to CloudShell bash terminal
3. Upload the file 'Get_OS_details.py" to CloudShell
4. Run the below commands after uploading:
   
   a. ```pip install azure-mgmt-compute azure-mgmt-resource azure-identity openpyxl```
   
   b. ```chmod 644 Get_OS_details.py```
   
   c.  ```python Get_OS_details.py```


## Output
The output of the above steps are stored in an excel file with the ```azure_vms_os_info.xlsx```.
