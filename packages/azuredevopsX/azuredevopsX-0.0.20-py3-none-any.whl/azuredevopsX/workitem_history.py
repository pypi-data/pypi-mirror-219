import logging
logging.basicConfig(level=logging.INFO)
from azuredevopsX.abstractdevops import AbstractDevOps
from azuredevopsX import factories

class WorkItemHistory(AbstractDevOps):

	def __init__(self,personal_access_token, organization_url):
		super(WorkItemHistory,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
		self.serviceWorkitem = factories.WorkItemFactory(personal_access_token=personal_access_token,organization_url=organization_url)
		

	def get_all (self, today=False):
		try:
			logging.info("Start function: WorkItemHistory")
			
			work_items_list = self.serviceWorkitem.get_all(today=today)
			revisions_list = []
			
			for work_item in work_items_list:
				logging.info("Getting Revisisons: "+work_item.fields['System.TeamProject']+"--"+str(work_item.id))
				revisions = self.work_item_tracking_client.get_revisions(project=work_item.fields['System.TeamProject'], id = work_item.id, expand="All")
				revisions_list.extend (revisions)
				

			return revisions_list

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	

	