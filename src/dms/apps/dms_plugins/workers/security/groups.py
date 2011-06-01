from django.contrib.auth.models import Group

from dms_plugins.pluginpoints import BeforeStoragePluginPoint, BeforeRetrievalPluginPoint
from dms_plugins.workers import Plugin, PluginError

class GroupSecurityStore(Plugin, BeforeStoragePluginPoint):
    name = 'Security Group'
    description = 'Security group member only'
    active = True

    def work(self, request, document):
        return GroupSecurity().work(request, document)

class GroupSecurityRetrieval(Plugin, BeforeRetrievalPluginPoint):
    name = 'Security Group'
    description = 'Security group member only'
    active = True
    index = 0

    def work(self, request, document):
        return GroupSecurity().work(request, document)

class GroupSecurity(object):
    def work(self, request, document, **kwargs):
        security_group, created = Group.objects.get_or_create(name='security')
        if not security_group in request.user.groups.all():
            raise PluginError("You're not in security group")
        return document