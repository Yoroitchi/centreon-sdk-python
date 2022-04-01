# -*- coding: utf-8 -*-

import centreonapi.webservice.configuration.common as common
from centreonapi.webservice import Webservice
from centreonapi.webservice.configuration.hostgroups import HostGroups

class ServiceGroup(common.CentreonObject):
    def __init__(self, properties):
        self.webservice = Webservice.getInstance()
        self.__clapi_action = 'SG'
        self.id = properties.get('id')
        self.name = properties.get('name')
        self.alias = properties.get('alias')
        self.comment = properties.get('comment')
        self.activate = properties.get('activate')

    def __repr__(self):
        return self.description

    def __str__(self):
        return self.description

    # Mais quel était le but ?
    def get(self, name):
        state, servicegroups = self.webservice.call_clapi(
                            'show',
                            self.__clapi_action)
        if state and len(servicegroups['result']) > 0:
            for sg in servicegroups['result']:
                service_obj = sg
                servicegroups[service_obj['name']] = service_obj
        try:
            return True, servicegroups[name] 
        except Exception:
            return False, 'not Found'
    
    def setparam(self, name, param, value):
        data = []
        values = [
            name,
            param,
            value
            ]
        status_add = self.webservice.call_clapi( 'setparam', self.__clapi_action, values)
        data.append("ServiceGroups setparam %s :%s" % (str(name) , str(status_add)))  
        return data

    def setservicetemplate(self, name, servicetemplate):
        data = []
        values = [
            name, 
            "|".join(common.build_param(servicetemplate))
            ]
        status_add = self.webservice.call_clapi('setservice', self.__clapi_action, values)
        data.append("ServiceGoup setservicetemplate  %s : %s :%s" % (name,str(values) ,str(status_add)))
        return data

class ServiceGroups(comon.CentreonDecorator, common.CentreonObject):
    """
    Centreon Web Service Groups object
    """
    def exist(self, name):
        if not self.servicegroup:
            self.list()
        if name in self.servicegroup:
            return True
        else:
            return False

    def __init__(self):
        super(ServiceGroups, self).__init__()
        self.servicegroup = {}
        self.__clapi_action = 'SG'

    def __contains__(self, name):
        return name in self.servicegroup.keys()

    def __getitem__(self, name):
        if not self.servicegroup:
            self.list()
        if name in self.servicegroup.keys():
            return True, self.servicegroup[name]
        else:
            return False, None

    @common.CentreonDecorator.pre_refresh
    def list(self):
        return self.servicegroup

    @common.CentreonDecorator.post_refresh
    def add(self, name, alias):   
        data = []
        values = [ name, alias]
        status_add = self.webservice.call_clapi('add', self.__clapi_action,values)
        data.append("ServiceGoup add %s :%s" % (name ,str(status_add)))
        return data

    @common.CentreonDecorator.post_refresh
    def delete(self, name):
        data = list()
        status_add = self.webservice.call_clapi('del', self.__clapi_action, name)
        data.append("ServiceGroup delete %s :%s" % (name ,str(status_add)))
        return data