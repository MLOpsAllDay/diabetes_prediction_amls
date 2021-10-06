from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core import Workspace
from AMLS_SDK import AmlsSdk
import os,json



def main(cluster_name:str,ws:Workspace)->None:
    try:
        # Check for existing compute target
        pipeline_cluster = ComputeTarget(workspace=ws, name=cluster_name)
        print('Found existing cluster, use it.')
    except ComputeTargetException:
        # If it doesn't already exist, create it
        try:
            compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS11_V2', max_nodes=2)
            pipeline_cluster = ComputeTarget.create(ws, cluster_name, compute_config)
            pipeline_cluster.wait_for_completion(show_output=True)
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    tenant_id = os.environ["TENANT_ID"]
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    subscription_id = os.environ["SUBSCRIPTION_ID"]
    resource_group = os.environ["RESOURCE_GROUP"]
    workspace_name = os.environ["WORKSPACE_NAME"]
    cluster_name = os.environ["COMPUTE_NAME"]

    amls = AmlsSdk(tenant_id,client_id,client_secret,
                    subscription_id,resource_group,workspace_name)

    ws = amls.ws

    main(cluster_name,ws)