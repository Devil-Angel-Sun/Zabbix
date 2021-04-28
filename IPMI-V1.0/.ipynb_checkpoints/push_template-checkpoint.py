import os, glob
from pyzabbix import ZabbixAPI

class Push_Template():
    '''
    主要用途：将模板推送到zabbix中
    参数:html: zabbix的网址
         user:zabbix的登录用户
         password: zabbix的登录密码
         path: xml文件的读取路径
    '''
    def __init__(self, html, user = 'Admin', password = 'zabbix', path = './templates_xml'):
        self.html = html
        self.user = user
        self.password = password
        self.path = path
        
    def login(self):
        zapi = ZabbixAPI(self.html)
        zapi.login(self.user, self.password)
        return zapi

    def rules(self):
        rules = {
            'applications': {
                'createMissing': True,
            },
            'discoveryRules': {
                'createMissing': True,
                'updateExisting': True
            },
            'graphs': {
                'createMissing': True,
                'updateExisting': True
            },
            'groups': {
                'createMissing': True
            },
            'hosts': {
                'createMissing': True,
                'updateExisting': True
            },
            'images': {
                'createMissing': True,
                'updateExisting': True
            },
            'items': {
                'createMissing': True,
                'updateExisting': True
            },
            'maps': {
                'createMissing': True,
                'updateExisting': True
            },
            'screens': {
                'createMissing': True,
                'updateExisting': True
            },
            'templateLinkage': {
                'createMissing': True,
            },
            'templates': {
                'createMissing': True,
                'updateExisting': True
            },
            'templateScreens': {
                'createMissing': True,
                'updateExisting': True
            },
            'triggers': {
                'createMissing': True,
                'updateExisting': True
            },
            'valueMaps': {
                'createMissing': True,
                'updateExisting': True
            },
        }
        return rules
    
    def push(self):
        zapi = self.login()
#         path = './templates_xml'
        if os.path.isdir(self.path):
            files = glob.glob(self.path+'/*.xml')
            for file in files:
                print(file)
                with open(file, 'r') as f:
                    template = f.read()
                    try:
                        zapi.confimport('xml', template, self.rules())
                    except ZabbixAPIException as e:
                        print(e)
        else:
            print('I need a xml file')
            
if __name__ == 'main__':
    html = "http://192.168.50.100:18080"
    pt = Push_Template(html)
    pt.push()