import logging
logging.basicConfig(level=logging.INFO)
from azuredevopsX.abstractdevops import AbstractDevOps
from azuredevopsX import factories
# Represent a type of Workitem 
class WorkItemType(AbstractDevOps):
	
	def __init__(self,personal_access_token, organization_url):
		super(WorkItemType,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
	

	def get_all(self, today = False):
		try:
			logging.info("Start function: get_work_item")
			logging.info("End function: get_work_item")
			project_service = factories.ProjectFactory(personal_access_token=self.personal_access_token,organization_url=self.organization_url)
			projects = project_service.get_all()
			result = []
			for project in projects:
				
				workitems = self.work_item_tracking_client.get_work_item_types(project.id)
				print (workitems)
				for workitem in workitems:
					workitem.additional_properties["project"] = project.__dict__
					result.append (workitem)
			return result
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 


	# Return workitem types
	def get_work_item_type(self,project):
		try:
			logging.info("Start function: get_work_item")
			logging.info("End function: get_work_item")
			return self.work_item_tracking_client.get_work_item_types(project)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 