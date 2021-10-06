from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core import Workspace
from AMLS_SDK import AmlsSdk
import os


def main(ws:Workspace,environment_name:str)->None:
    # Create a Python environment for the experiment
    diabetes_env = Environment(environment_name)
    diabetes_env.python.user_managed_dependencies = False # Let Azure ML manage dependencies
    diabetes_env.docker.enabled = True # Use a docker container

    # Create a set of package dependencies
    diabetes_packages = CondaDependencies.create(conda_packages=['scikit-learn','ipykernel','matplotlib','pandas','pip'],
                                                 pip_packages=['azureml-defaults','azureml-dataprep[pandas]','pyarrow'])

    # Add the dependencies to the environment
    diabetes_env.python.conda_dependencies = diabetes_packages

    # Register the environment
    diabetes_env.register(workspace=ws)


    print ("Run configuration created.")

if __name__ == "__main__":
    tenant_id = os.environ["TENANT_ID"]
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    subscription_id = os.environ["SUBSCRIPTION_ID"]
    resource_group = os.environ["RESOURCE_GROUP"]
    workspace_name = os.environ["WORKSPACE_NAME"]
    environment_name = os.environ["ENVIRONMENT_NAME"]

    amls = AmlsSdk(tenant_id,client_id,client_secret,
                    subscription_id,resource_group,workspace_name)

    ws = amls.ws
    main(ws,environment_name)