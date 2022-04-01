# -*- coding: utf-8 -*-

import centreonapi.webservice.configuration.common as common
from centreonapi.webservice import Webservice

class ServiceTemplate(common.CentreonObject):
    def __init__(self, properties):
        self.webservice = Webservice.getInstance()
        self.__clapi_action = 'STPL'
        self.id = properties.get('id')
        self.name = properties.get('name')
        self.alias = properties.get('alias')
        self.active_check_enabled = properties.get('active checks enabled')
        self.check_command = properties.get('check command')
        self.check_command_args = properties.get('check_command_args')
        self.max_check_attempts = properties.get('max check attempts')
        self.normal_check_interval = properties.get('normal check interval')
        self.passive_checks_enabled = properties.get('passive checks enabled')
        self.retry_check_interval = properties.get('retry check interval')
        self.macros = {}
        self.hostgroups = {}
        self.contacts = {}

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Servicetemplates(common.CentreonDecorator, common.CentreonObject):