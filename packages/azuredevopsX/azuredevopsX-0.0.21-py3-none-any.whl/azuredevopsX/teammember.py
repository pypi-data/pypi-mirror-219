import logging
logging.basicConfig(level=logging.INFO)
from azuredevopsX.abstractdevops import AbstractDevOps
from azuredevopsX import factories

# Represent a team member
class TeamMember(AbstractDevOps):

	def __init__(self,personal_access_token, organization_url):
		super(TeamMember,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
	
	def get_team_members(self, project_id, team_id):
		return self.core_client.get_team_members_with_extended_properties(project_id=project_id,team_id=team_id)
    
	def get_all(self, today = False):
		project_service = factories.ProjectFactory(personal_access_token=self.personal_access_token,organization_url=self.organization_url)
		projects = project_service.get_all()
			
		all_team_members = []
        
		for project in projects:
			teams = self.core_client.get_teams(project.id)
			for team in teams:
				team_members = self.get_team_members(project.id,team.id)
				for team_member in team_members:
					team_member.additional_properties["project"] = project.__dict__
					team_member.additional_properties["team"] = team.__dict__
					team_member.identity = team_member.identity.__dict__
					team_member.identity["_links"] = team_member.identity["_links"].__dict__
					all_team_members.append(team_member)
		
		return all_team_members