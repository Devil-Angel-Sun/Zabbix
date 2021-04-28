import pandas as pd
from xml.dom import minidom
import json

class Create_IPMI:
    '''
    主要作用：生成ipmi的ipmi.get的模板文件，以获取主机的ipmi数据
    参数:save_xml：生成xml文件的路径
    '''
    def __init__(self, save_xml = './templates_xml/ipmi_get.xml'):
        self.save_xml = save_xml
    
    def create_ipmi_template(self):
        dom = minidom.Document()
        root_node = dom.createElement('zabbix_export')
        dom.appendChild(root_node)

        root_node.appendChild(dom.createElement('version')).appendChild(dom.createTextNode('5.0'))
        root_node.appendChild(dom.createElement('groups')).appendChild(dom.createElement('group')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI'))
        template = root_node.appendChild(dom.createElement('templates')).appendChild(dom.createElement('template'))
        template.appendChild(dom.createElement('template')).appendChild(dom.createTextNode('Template ipmi_get of IPMI'))
        template.appendChild(dom.createElement('name')).appendChild(dom.createTextNode('Template ipmi_get of IPMI'))
        template.appendChild(dom.createElement('groups')).appendChild(dom.createElement('group')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI'))
        template.appendChild(dom.createElement('applications')).appendChild(dom.createElement('application')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI_LLD'))
        template_item = template.appendChild(dom.createElement('items')).appendChild(dom.createElement('item'))
        dict_item = {'name':'IPMI Discovery', 'type' : 'IPMI', 'key': 'ipmi.get', 'history' : '2h', 'value_type' : 'TEXT'}
        for i in dict_item:
            template_item.appendChild(dom.createElement(i)).appendChild(dom.createTextNode(dict_item[i]))
        template_item.appendChild(dom.createElement('applications')).appendChild(dom.createElement('application')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI_LLD'))
        return dom
    
    def save_ipmi(self):
        dom = self.create_ipmi_template()
        try:
            with open(self.save_xml, 'w', encoding = 'UTF-8') as fh:
                dom.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
                #print('写入xml OK!')
        except Exception as err:
            print('错误信息：{0}'.format(err))
            
if __name__ == '__main__':
    ci = Create_IPMI()
    ci.save_ipmi()