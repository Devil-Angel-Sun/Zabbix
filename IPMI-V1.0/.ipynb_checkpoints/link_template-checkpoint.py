from pyzabbix import ZabbixAPI
from get_information import Get_message
import sched, time, os,json, glob, re
import pandas as pd

class Link_Template():
    def __init__(self, excel_path, html, user = 'Admin', password = 'zabbix', xml_files = './templates_xml/'):
        self.excel_path = excel_path
        self.html = html
        self.user = user
        self.password = password
        self.xml_files = xml_files
        
    def login(self):
        zapi = ZabbixAPI(self.html)
        zapi.login(self.user, self.password)
        return zapi
        
    def compare(self):
        files = glob.glob(self.xml_files+'*.xml')
        files_list =[]
        for i in files:
            if re.compile('^[0-9]{1}.*$').match(i.split('/')[-1]): # 判断是否以数字开头
                files_list.append(i)
        return files_list
    
    def get_hostid(self):
        gm = Get_message(excel_path = self.excel_path, html = self.html)
        host_ids = gm.get_hosts_id()
        return host_ids
    
    def get_template_id(self, template):
        '''获取所有模板的id和名字信息,并取出所需模板的templateid'''
        zapi = self.login()
        template_list = zapi.template.get(output=["templateid","name"])
        name = 'Template ' + template.split('/')[-1].split('.xml')[0]+' of IPMI'
        return int([i['templateid'] for i in template_list if i['name'] == name][0])
    
    def link(self):
        zapi = self.login()
        files_list = self.compare()
        host_ids = self.get_hostid()
        for templateid in files_list:
            for hostid in host_ids:
                if templateid.split('/')[-1].split('.xml')[0].split('_')[1] == host_ids[hostid]:
                    zapi.template.massadd(templates = self.get_template_id(templateid), hosts={"hostid": hostid})

if __name__ == '__main__':
    lt = Link_Template(excel_path = './host.xlsx', html = "http://192.168.50.100:18080")
    lt.link()