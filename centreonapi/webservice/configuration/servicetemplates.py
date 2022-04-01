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

    def get(self, description):
        stpls = []
        state, stpls = self.webservice.call_clapi(show, self.__clapi_action)
        if state and len(stpls['result']) > 0:
            for s in spls['result']:
                stpl_obj = s
                stpls[stpl_obj.get('description')] = stpl_obj
        try:
            return True, stpls[description]
        except Exception:
            return False, 'stpls[description] Not Found'

    def setmacro(self, name, macro, value, is_password=None, desc=None):
            if desc is None:
                desc = ''
            if is_password is None:
                is_password = 0
            data = {}    
            macro = macro.replace("_HOST", "").replace("$", "").upper()
            values = [name, macro, value, is_password, name]
            status_add = self.webservice.call_clapi('setmacro', self.__clapi_action, values)
            data.append("ServiceTemplate setmacro: %s" % str(status_add))

    def set_check_command_args(self, name, value):
                data = []
                value = value.replace("\'", "\"")
                stud_obj = json.loads(value) 
                my_list = []
                for i in stud_obj:
                    for key,value in i.items() :
                        my_list.append(value)
                values = [name, 'check_command_arguments', "!"+"!".join(my_list)]
                status_add = self.webservice.call_clapi('setparam', self.__clapi_action, values) 
                data.append("ServiceTemplate set_check_command_arguments: %s" % str(status_add))

    def setparam(self, name, param, value):
        data = []
        values = [name, param, value]
        status_add = self.webservice.call_clapi('setparam', self.__clapi_action, values)
        data.append("ServiceTemplate setparam :%s" % str(status_add))
        return data

    def sethosttemplate(self, name, hosttemplate):
        data = []
        values = [name, "|".join(common.build_param(hosttemplate))]
        status_add = self.webservice.call_clapi('sethosttemplate', self.__clapi_action, values)
        data.append("ServiceTemplate sethosttemplate  %s: %s" % (name ,str(status_add)))
        return data

    def setcontacts(self, name, contacts):
        data = []
        values = [name, "|".join(common.build_param(contacts))]
        status_add = self.webservice.call_clapi('setcontact', self.__clapi_action, values)
        data.append("ServiceTemplate setcontact %s: %s" % (name ,str(status_add)))
        return data

    def setcontactgroup(self, name, contactsgroup):
        data = []
        values = [name, "|".join(common.build_param(contactsgroup))]
        status_add = webservice.call_clapi('setcontactgroup', self.__clapi_action, values)
        data.append("ServiceTemplate setcontactgroup  %s: %s" % (name ,str(status_add)))
        return data

    def settrap(self, name, trap):
        data = []
        values = [name, "|".join(common.build_param(trap))]
        status_add = webservice.call_clapi('settrap', self.__clapi_action, values)
        data.append("ServiceTemplate trap  %s: %s" % (name ,str(status_add)))
        return data

    def addservicetemplate(self, name, alias=None, servicetemplate=None):
        data = list()
        values = [name, alias, servicetemplate]
        status_add = self.webservice.call_clapi('add', self.__clapi_action, values)
        data.append("ServiceTemplate %s: %s" % (name ,str(status_add)))
        return data

class ServiceTemplates(common.CentreonDecorator, common.CentreonObject):
    def exist(self, name):
        if not self.serviceTemplates:
            self.list()
        if name in self.serviceTemplates:
            return True
        else:
            return False

    def __init__(self):
        super(ServiceTemplates, self).__init__()
        self.serviceTemplates = {}
        self.__clapi_action = 'STPL'

    def __contains__(self, name):
        return name in self.stpls.keys()

    def __getitem__(self, name):
        if not self.serviceTemplates:
            self.list()
        if name in self.serviceTemplates.keys():
            return True, self.serviceTemplates[name]
        else:
            return False, None

    @common.CentreonDecorator.pre_refresh
    def list(self):
        return self.serviceTemplates

    @common.CentreonDecorator.post_refresh
    def add(self, name, alias=None):
        data = []
        values = [
                name, 
                alias, 
                ''
                ]
        status_add = self.webservice.call_clapi('add', self.__clapi_action, values)
        data.append("ServiceTemplate add %s: %s" % (name, str(status_add)))
        return data

    @common.CentreonDecorator.post_refresh
    def delete(self, name):
        data = []
        status_add = self.webservice.call_clapi('del', self.__clapi_action, name)
        data.append("ServiceTemplate delete %s: %s" % (name, str(status_add)))
        return data