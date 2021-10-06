
from azureml.core import Workspace
from azureml.pipeline.core import Pipeline
from azureml.widgets import RunDetails
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration
from azureml.core import Environment
from AMLS_SDK import AmlsSdk
import os

def main(ws:Workspace,compute_name:str,environment_name:str,experiment_folder:str,dataset_name:str,endpoints_name:str)->None:
    # Get the training dataset
    diabetes_ds = ws.datasets.get(dataset_name)

    registered_env = Environment.get(ws, environment_name)

    # Create a new runconfig object for the pipeline
    pipeline_run_config = RunConfiguration()

    # Use the compute you created above.
    pipeline_run_config.target = compute_name

    # Assign the environment to the run configuration
    pipeline_run_config.environment = registered_env
    # Create a PipelineData (temporary Data Reference) for the model folder
    prepped_data_folder = PipelineData("prepped_data_folder", datastore=ws.get_default_datastore())

    # Step 1, Run the data prep script
    train_step = PythonScriptStep(name = "Prepare Data",
                                    source_directory = experiment_folder,
                                    script_name = "prep_diabetes.py",
                                    arguments = ['--input-data', diabetes_ds.as_named_input('raw_data'),
                                                 '--prepped-data', prepped_data_folder],
                                    outputs=[prepped_data_folder],
                                    compute_target = compute_name,
                                    runconfig = pipeline_run_config,
                                    allow_reuse = True)

    # Step 2, run the training script
    register_step = PythonScriptStep(name = "Train and Register Model",
                                    source_directory = experiment_folder,
                                    script_name = "train_diabetes.py",
                                    arguments = ['--training-folder', prepped_data_folder],
                                    inputs=[prepped_data_folder],
                                    compute_target = compute_name,
                                    runconfig = pipeline_run_config,
                                    allow_reuse = True)

    print("Pipeline steps defined")
    # Construct the pipeline
    pipeline_steps = [train_step, register_step]
    pipeline = Pipeline(workspace=ws, steps=pipeline_steps)
    print("Pipeline is built.")

    pipeline.publish(endpoints_name)
    print("endpoint published")

if __name__ == "__main__":
    tenant_id = os.environ["TENANT_ID"]
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    subscription_id = os.environ["SUBSCRIPTION_ID"]
    resource_group = os.environ["RESOURCE_GROUP"]
    workspace_name = os.environ["WORKSPACE_NAME"]
    cluster_name = os.environ["COMPUTE_NAME"]
    environment_name = os.environ["ENVIRONMENT_NAME"]
    pipeline_endpoint = os.environ["PIPELINE_ENDPOINT"]
    dataset_name = os.environ["DATASET_NAME"]
    scripts_path = os.environ["SCRIPTS_PATH"]

    amls = AmlsSdk(tenant_id,client_id,client_secret,
                    subscription_id,resource_group,workspace_name)

    ws = amls.ws

    main(ws,cluster_name,environment_name,scripts_path,dataset_name,pipeline_endpoint)