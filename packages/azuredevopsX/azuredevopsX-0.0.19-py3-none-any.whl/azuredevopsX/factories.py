import factory
from .project import Project
from .backlog import Backlog
from .identity import Identity
from .interaction import Interaction
from .status import Status
from .team import Team
from .teammember import TeamMember
from .workitem import WorkItem
from .workitemtype import WorkItemType
from .workitem_history import WorkItemHistory

class WorkItemHistoryFactory(factory.Factory):
    
    class Meta:
        model = WorkItemHistory
        
    personal_access_token = None
    organization_url = None

class ProjectFactory(factory.Factory):
    
    class Meta:
        model = Project
        
    personal_access_token = None
    organization_url = None

class BacklogFactory(factory.Factory):
    
    class Meta:
        model = Backlog
    personal_access_token = None
    organization_url = None

class IdentityFactory(factory.Factory):
    
    class Meta:
        model = Identity
    personal_access_token = None
    organization_url = None

class InteractionFactory(factory.Factory):
    
    class Meta:
        model = Interaction
    personal_access_token = None
    organization_url = None

class StatusFactory(factory.Factory):
    
    class Meta:
        model = Status
    personal_access_token = None
    organization_url = None

class TeamFactory(factory.Factory):
    
    class Meta:
        model = Team
    personal_access_token = None
    organization_url = None

class TeamMemberFactory(factory.Factory):
    
    class Meta:
        model = TeamMember
    personal_access_token = None
    organization_url = None


class WorkItemFactory(factory.Factory):
    
    class Meta:
        model = WorkItem
    personal_access_token = None
    organization_url = None


class WorkItemTypeFactory(factory.Factory):
    
    class Meta:
        model = WorkItemType
    personal_access_token = None
    organization_url = None