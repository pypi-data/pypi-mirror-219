import logging
logging.basicConfig(level=logging.INFO)
from azuredevopsX.abstractdevops import AbstractDevOps

# TODO
class Identity(AbstractDevOps):
	
	def __init__(self,personal_access_token, organization_url):
		super(Identity,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
