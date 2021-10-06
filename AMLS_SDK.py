from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication

class AmlsSdk():

    def __init__(self,tenant_id:str,client_id:str,client_secret:str,
                subscription_id:str,resource_group:str,workspace_name:str)->Workspace:
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name

        sp_auth = ServicePrincipalAuthentication(self.tenant_id,self.client_id,self.client_secret)

        self.ws = Workspace(self.subscription_id,self.resource_group,self.workspace_name,sp_auth)


