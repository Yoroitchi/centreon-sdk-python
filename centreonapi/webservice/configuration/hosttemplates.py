# -*- coding: utf-8 -*-

import centreonapi.webservice.configuration.common as common
from centreonapi.webservice import Webservice
from centreonapi.webservice.configuration.hostgroups import HostGroups

class HostTemplate(common.CentreonObject):
    def __init__(self, properties):
        self.webservice = Webservice.getInstance()
        self.__clapi_action = 'HTPL'
        self.id = properties.get('id')
        self.name = properties.get('name')
        self.activate = properties.get('activate')
        self.address = properties.get('address')
        self.alias = properties.get('alias')
        self.macros = {}
        self.templates = {}
        self.hostTemplate = {}
        self.parent = {}
        self.hostGroups = {}
        self.contactGroups = {}
        self.contacts = {}
        self.params = {}
        self.state = properties.get('state')
    
    # A quoi sert cette fonction ?
    def set_check_command_args(self, description, value):
        data = []
        value = value.replace("\'", "\"")
        stud_obj = json.loads(value)
        my_list = []
        for i in stud_obj:
            for key, value in i.items():
                my_list.append(value)
        values = [
            description,
            'check_command_arguments',
            "!" + "!".join(my_list)
        ]
        status_add = self.webservice.call_clapi(
            'setparam',
            self.__clapi_action,
            values
        )
        data.append("check_command_argument: %s" % str(status_add))

    def setmacro(self, description, macro, value, is_password=None, desc=None):
        if desc is None:
            desc = ''
        if is_password is None:
            is_password = 0
        data = []
        macro = macro.replace("_HOST", "").replace("$", "").upper()
        values = [description, macro, value, is_password, desc]
        return self.webservice.call_clapi('set_macro', self.__clapi_action, values)

    def setparam(self, description, param, value):
        data = []
        values = [description, param, value]
        status_add = self.webservice.call_clapi('setparam', self.__clapi_action, values)
        data.append("notification_period: %s" % str(status_add))
        return data

    def sethosttemplate(self, description, hosttemplate):
        data = {}
        values = [
                description,
                "|".join(common.build_param(hosttemplate))
                ]
        status_add = self.webservice.call_clapi('sethosttemplate', self.__clapi_action, values)
        data.append("HostTemplate sethosttemplate  %s :%s" % (description ,str(status_add)))
        return data

    def setcontact(self, description, contact):
        data = []
        values = [description, 
                "|".join(common.build_param(contact))]
        status_add = self.webservice.call_clapi('setcontact', self.__clapi_action, values)
        data.append("HostTemplate setcontact %s: %s" % (description, str(status_add)))
        return data

    def setcontactgroup(self, description, contactgroup):
        data = []
        values = [description, 
                "|".join(common.build_param(contactgroup))]
        status_add = self.webservice.call_clapi('setcontactgroup', self.__clapi_action, values)
        data.append("HostTemplate setcontactgroup %s: %s" % (description, str(status_add)))
        return data

    def gethostgroup(self, name):
        data = []
        hostgroup = {}
        state, hgs = self.webservice.call_clapi('gethostgroup', self.__clapi_action, name)
        data.append("HostTemplate gethostgroup %s" % (str(hgs)))
        if state:
            if len(hgs['result']) > 0:
                for h in hgs['result']:
                    hg_obj = HostGroup(h)
                    self.hostGroups[hg_obj.name] = hg_obj
                return state, self.hostGroups
            else:
                return state, None
        else:
            return state, hgs            

    def sethostgroup(self, description, hostgroup=None):
        data = []
        values = [description, 
                "|".join(common.build_param(hostgroup))]
        status_add = self.webservice.call_clapi('sethostgroup', self.__clapi_action, values)
        data.append("HostTemplate sethostgroup %s: %s" % (description, str(status_add)))

    def deletehostgroup(self, description, hostgroup=None):
        data = []
        values = [description, 
                "|".join(common.build_param(hostgroup))]
        status_add = self.webservice.call_clapi('delhostgroup', self.__clapi_action, values)
        data.append("HostTemplate delhostgroup %s: %s" % (description, str(status_add)))
 
    

class HostTemplates(common.CentreonDecorator, common.CentreonObject):
    def __init__(self):
        super(HostTemplates, self).__init__()
        self.HostTemplates = {}
        self.__clapi_action = 'HTPL'

    def exist(self, name):
        if not self.HostTemplates:
            self.list()
        if name in self.HostTemplates:
            return True
        else:
            return False

    def __contains__(self, name):
        return name in self.HostTemplates.keys()

    def __getitem__(self, name):
        if not self.HostTemplates:
            self.list()
        if name in self.HostTemplates.keys():
            return True, self.HostTemplates[name]
        else:
            return False
    
    @common.CentreonDecorator.pre_refresh
    def list(self):
        return self.HostTemplates

    @common.CentreonDecorator.post_refresh
    def add(self, name, alias, ip, instance=None, template=None, hg=None):
        data = []
        values = [
                name, 
                alias, 
                ip, 
                str("|".join(common.build_param(template))) if template else template, 
                str(common.build_param(instance)[0]) if instance else "Central", 
                str("|".join(common.build_param(hg))) if hg else hg
                ]
        status_add = self.webservice.call_clapi('add', self.__clapi_action, values)
        data.append("HostTemplate add %s: %s" % (name, str(status_add)))
        return data

    @common.CentreonDecorator.post_refresh
    def delete(self, description):
        data = []
        status_add = self.webservice.call_clapi('del', self.__clapi_action, description)
        data.append("HostTemplate del %s: %s" % (description, str(status_add)))
        return data