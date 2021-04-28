import pandas as pd
from xml.dom import minidom

class Create_host:
    '''
    主要作用：通过输入的表格用于输出host的xml文件
    参数: excel_path:输入表格的文件路径（含文件）
         xml_path:输出xml的文件路径(含文件名)
    '''
    def __init__(self, excel_path, xml_path = './templates_xml/host.xml'):
        self.excel_path = excel_path
        self.xml_path = xml_path
        
    def get_data(self):    
        data = pd.read_excel(self.excel_path)
        return data
    
    def create_template(self):
        data = self.get_data()
        dom = minidom.Document()
        root_node = dom.createElement('zabbix_export')
        dom.appendChild(root_node)
        root_node.appendChild(dom.createElement('version')).appendChild(dom.createTextNode('5.0'))
        root_node.appendChild(dom.createElement('groups')).appendChild(dom.createElement('group')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI'))
        hosts = root_node.appendChild(dom.createElement('hosts'))
        for i in range(data.shape[0]):
            host = hosts.appendChild(dom.createElement('host'))
            host.appendChild(dom.createElement('host')).appendChild(dom.createTextNode(data.loc[i]['host']))
            host.appendChild(dom.createElement('name')).appendChild(dom.createTextNode(data.loc[i]['name']))
            host.appendChild(dom.createElement('ipmi_username')).appendChild(dom.createTextNode(data.loc[i]['username']))
            host.appendChild(dom.createElement('ipmi_password')).appendChild(dom.createTextNode(data.loc[i]['password']))
            host.appendChild(dom.createElement('groups')).appendChild(dom.createElement('group')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI'))
            interface = host.appendChild(dom.createElement('interfaces')).appendChild(dom.createElement('interface'))
            interface.appendChild(dom.createElement('type')).appendChild(dom.createTextNode('IPMI'))
            interface.appendChild(dom.createElement('ip')).appendChild(dom.createTextNode(data.loc[i]['host']))
            interface.appendChild(dom.createElement('port')).appendChild(dom.createTextNode('623'))
            interface.appendChild(dom.createElement('interface_ref')).appendChild(dom.createTextNode('if1'))
            host.appendChild(dom.createElement('inventory_mode')).appendChild(dom.createTextNode('DISABLED'))
        return dom
        
    def save_host(self):
        dom = self.create_template()
        try:
            with open(self.xml_path,'w',encoding='UTF-8') as fh:
                dom.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
                #print('写入xml OK!')
        except Exception as err:
            print('错误信息：{0}'.format(err))

if __name__ == '__main__':
    excel_path = './host.xlsx'
    ch = Create_host(excel_path = excel_path)
    ch.save_host()