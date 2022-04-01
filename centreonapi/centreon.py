# -*- coding: utf-8 -*-

from centreonapi.webservice.configuration.host import Hosts
from centreonapi.webservice.configuration.hosttemplates import HostTemplates
from centreonapi.webservice.configuration.poller import Pollers
from centreonapi.webservice.configuration.hostgroups import HostGroups
from centreonapi.webservice.configuration.command import Commands
from centreonapi.webservice.configuration.resourcecfg import ResourceCFGs
from centreonapi.webservice.configuration.servicegroups import ServiceGroups
from centreonapi.webservice.configuration.servicetemplates import ServiceTemplates
from centreonapi.webservice import Webservice


class Centreon(object):

    def __init__(self, url=None, username=None, password=None, check_ssl=True):
        Webservice.getInstance(
            url,
            username,
            password,
            check_ssl
        )

        self.hosts = Hosts()
        self.pollers = Pollers()
        self.hostgroups = HostGroups()
        self.hosttemplates = HostTemplates()
        self.commands = Commands()
        self.resourcecfgs = ResourceCFGs()
        self.servicegroups = ServiceGroups()
