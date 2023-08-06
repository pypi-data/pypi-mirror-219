from azure.devops.credentials import BasicAuthentication
from azure.devops.connection import Connection
from azure.devops.v5_1.work.models import TeamContext
from azure.devops.v5_1.client_factory import ClientFactoryV5_1
from azure.devops.v5_1.work_item_tracking import WorkItemTrackingClient 
from azure.devops.v5_1.work_item_tracking.models import Wiql
from pprint import pprint
from abc import ABC

class AbstractDevOps(ABC):

    def __init__(self, personal_access_token, organization_url):

        self.personal_access_token = personal_access_token
        self.organization_url = organization_url

        self.credentials = BasicAuthentication('', personal_access_token)
        self.connection = Connection(base_url=organization_url, creds=self.credentials)

        self.core_client = self.connection.clients.get_core_client()
        self.work_client = self.connection.clients_v5_1.get_work_client()
        self.work_item_tracking_client = self.connection.clients_v5_1.get_work_item_tracking_client()
        self.work_item_process_tracking_client = self.connection.clients_v5_1.get_work_item_tracking_process_client()
    
    def create_team_context(self, project, team):
        return  TeamContext(project, project.id, team, team.id)
        
    