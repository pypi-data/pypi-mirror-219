import logging
logging.basicConfig(level=logging.INFO)
from azuredevopsX.abstractdevops import AbstractDevOps
from azure.devops.v5_1.work_item_tracking import WorkItemTrackingClient 
from azure.devops.v5_1.work_item_tracking.models import Wiql
from azuredevopsX import factories

# Represent a item of work in a project xxx

class WorkItem(AbstractDevOps):

	def __init__(self,personal_access_token, organization_url):
		super(WorkItem,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
	

	def get_all (self, today=False):
		try:
			logging.info("Start function: get_work_items")
			
			work_items_list = []
			work_items = None
			if today:
				work_items = self.get_query_today()
			else:
				work_items = self.get_work_item_query_by_wiql()
			
			# Dividindo em vetores de no máximo 200 itens. O serviço permite no máximo 200 ids por requisição;
			work_items_list_split = [work_items[x:x+200] for x in range(0,len(work_items), 200)]

			for work_items_list_item in work_items_list_split:
				
				work_item_list_retrieve = []
				#criando o vertor a ser enviado
				for work_item in work_items_list_item:
					work_item_list_retrieve.append(int(work_item.id))
				
				work_item_retrieved = self.get_work_items(ids=[*work_item_list_retrieve])				
				
				work_items_list.extend(work_item_retrieved)
			
			logging.info("End function: get_work_items")
			return work_items_list

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	

	# Return a specifc workitem from a project with detais
	def get_work_items(self,ids):
		try:
			logging.info("Start function: get_work_items")
			result = self.work_item_tracking_client.get_work_items(ids=ids, 
                                                        project=None,                                                       
                                                       expand="All")
			logging.info("End function: get_work_items")

			list_result = []
			
			for item in result:
				item._links = item._links.__dict__

				if item.comment_version_ref is not None:
					item.comment_version_ref = item.comment_version_ref.__dict__

				if item.relations is not None:
					item_relations = []
					
					for relation in item.relations:
						item_relations.append(relation.__dict__)
					
					item.relations = item_relations
			
				list_result.append(item)
			return list_result
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
		
	
	# Return a specifc workitem from a project with detais
	def get_work_item(self,work_item_id):
		try:
			logging.info("Start function: get_work_item")
			logging.info("End function: get_work_item")

			return self.work_item_tracking_client.get_work_item(id=work_item_id, 
                                                        project=None,                                                       
                                                       expand="All")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 


	def get_relation(self, relation):
		try:
			logging.info("Start function: get_work_item")
			logging.info("End function: get_work_item")

			return self.work_item_tracking_client.get_relation_type(relation)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
    
	def get_backlog_work_items(self, project,team, backlog):
		try:
			logging.info("Start function: get_work_item")
			logging.info("End function: get_work_item")
			team_context = self.create_team_context(project, team)
			return self.work_client.get_backlog_level_work_items(team_context, backlog.id)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def get_work_item_query_by_wiql(self):
		try:
			wiql = Wiql(
			query="""select 
					*
					from WorkItems"""
					
				)
			wiql_results = self.work_item_tracking_client.query_by_wiql(wiql).work_items
			if wiql_results:
				return wiql_results
			else:
				return []
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 	

	def get_query_today(self):
		try:
			wiql = Wiql(
			query="""select 
					*
					from WorkItems
					where 
					[System.CreatedDate] = @Today 
					OR [System.ChangedDate] = @Today 
					OR [Microsoft.VSTS.Common.ClosedDate] = @Today 
					OR [Microsoft.VSTS.Common.ResolvedDate] = @Today
					OR [System.RevisedDate] = @Today
					OR [Microsoft.VSTS.Common.StateChangeDate]= @Today
					order by [System.ChangedDate] desc"""
				)
			wiql_results = self.work_item_tracking_client.query_by_wiql(wiql).work_items
			if wiql_results:
				return wiql_results
			else:
				return []
		
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
	
	
	
	def get_work_item_query_by_wiql_epic_user_story_product_backlog_item(self):
		try:
			wiql = Wiql(
			query="""select 
					*
					from WorkItems
					order by [System.ChangedDate] desc"""
					
				)
			wiql_results = self.work_item_tracking_client.query_by_wiql(wiql).work_items
			if wiql_results:
				return wiql_results
			else:
				return []
		
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def get_work_item_query_by_wiql_task(self):
		try:
			wiql = Wiql(
			query="""
					select [System.Id],
						[System.WorkItemType],
						[System.Title],
						[System.State],
						[System.AreaPath],
						[System.IterationPath],
						[System.Tags],
						[System.TeamProject]
					from WorkItems
					where 
					[System.WorkItemType] = 'Task' 
					order by [System.ChangedDate] desc"""
				)
			wiql_results = self.work_item_tracking_client.query_by_wiql(wiql).work_items
			if wiql_results:
				return wiql_results
			else:
				return []

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def get_work_item_query_by_wiql(self):
		try:
			wiql = Wiql(
			query="""
					select [System.Id],
						[System.WorkItemType],
						[System.Title],
						[System.State],
						[System.AreaPath],
						[System.IterationPath],
						[System.Tags]
					from WorkItems
					order by [System.ChangedDate] desc"""
				)
			wiql_results = self.work_item_tracking_client.query_by_wiql(wiql).work_items
			if wiql_results:
				return wiql_results
			else:
				return []
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 