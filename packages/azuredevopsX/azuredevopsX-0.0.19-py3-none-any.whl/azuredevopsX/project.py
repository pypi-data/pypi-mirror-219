import logging
logging.basicConfig(level=logging.INFO)
from azuredevopsX.abstractdevops import AbstractDevOps

# Represents a software Project
class Project(AbstractDevOps):

	def __init__(self,personal_access_token, organization_url):
		super(Project,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
	
	# Returns a list of project
	def get_all(self, today=False): 
		projects = []
		try:
			logging.info("Start function: get_projects")
			
			get_projects_response = self.core_client.get_projects()
			
			while get_projects_response is not None:
				
				for project in get_projects_response.value:
					projects.append(project)
				if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
					# Get the next page of projects
					get_projects_response = self.core_client.get_projects(continuation_token=get_projects_response.continuation_token)
				else:
					# All projects have been retrieved
					get_projects_response = None

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Projects")
		
		return projects

	def get_processes(self):
		return self.work_item_process_tracking_client.get_list_of_processes()

	def get_process_behaviors(self, process_id):
		return self.work_item_process_tracking_client.get_process_behaviors(process_id)
    
	def get_process_by_its_id(self, process_type_id):
		return self.work_item_process_tracking_client.get_process_by_its_id(process_type_id)
    
	def get_state_definitions(self, process_id):
		return self.work_item_process_tracking_client.get_state_definitions(process_id)