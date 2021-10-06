from azureml.core import Dataset,Workspace
from AMLS_SDK import AmlsSdk
import os

def main(ws:Workspace,dataset_name:str)->None:
    default_ds = ws.get_default_datastore()

    if dataset_name not in ws.datasets:
        default_ds.upload_files(files=['./drop/data/diabetes.csv', './drop/data/diabetes2.csv'], # Upload the diabetes csv files in /data
                            target_path='diabetes-data/', # Put it in a folder path in the datastore
                            overwrite=True, # Replace existing files of the same name
                            show_progress=True)

        #Create a tabular dataset from the path on the datastore (this may take a short while)
        tab_data_set = Dataset.Tabular.from_delimited_files(path=(default_ds, 'diabetes-data/*.csv'))

        # Register the tabular dataset
        try:
            tab_data_set = tab_data_set.register(workspace=ws,
                                    name=dataset_name,
                                    description='diabetes data',
                                    tags = {'format':'CSV'},
                                    create_new_version=True)
            print('Dataset registered.')
        except Exception as ex:
            print(ex)
    else:
        print('Dataset already registered.')

if __name__ == "__main__":
    tenant_id = os.environ["TENANT_ID"]
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    subscription_id = os.environ["SUBSCRIPTION_ID"]
    resource_group = os.environ["RESOURCE_GROUP"]
    workspace_name = os.environ["WORKSPACE_NAME"]
    dataset_name = os.environ["DATASET_NAME"]

    amls = AmlsSdk(tenant_id,client_id,client_secret,
                    subscription_id,resource_group,workspace_name)

    ws = amls.ws
    main(ws,dataset_name)