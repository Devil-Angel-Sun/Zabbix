import pandas as pd
from xml.dom import minidom
# from pyzabbix import ZabbixAPI
import json,os
# zapi = ZabbixAPI('http://192.168.50.100:18080')
# zapi.login('Admin','zabbix')

class Create_Template():
    def __init__(self, json_file, save_path = './templates_xml/'):
        self.json_file = json_file
        self.save_path = save_path
        
    def get_data(self):
        data = pd.read_json(self.json_file)
        return data
    
    def create_xml(self):
        data = self.get_data()
        dom = minidom.Document()
        root_node = dom.createElement('zabbix_export')
        dom.appendChild(root_node)
        
        root_node.appendChild(dom.createElement('version')).appendChild(dom.createTextNode('5.0'))
        root_node.appendChild(dom.createElement('groups')).appendChild(dom.createElement('group')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI'))
        template = root_node.appendChild(dom.createElement('templates')).appendChild(dom.createElement('template'))
        template.appendChild(dom.createElement('template')).appendChild(dom.createTextNode('Template '+self.json_file.split('/')[-1].split('.json')[0]+' of IPMI'))
        template.appendChild(dom.createElement('name')).appendChild(dom.createTextNode('Template '+self.json_file.split('/')[-1].split('.json')[0]+' of IPMI'))
        template.appendChild(dom.createElement('groups')).appendChild(dom.createElement('group')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI'))
        
        applications = []
        for i in data['sensor']:
            applications.append(i['text'])
        applications = list(set(applications))
        applications.append('IPMI_LLD')
        
        template_applications = template.appendChild(dom.createElement('applications'))
        for application in applications:
            template_applications.appendChild(dom.createElement('application')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode(application))
        applications.remove('IPMI_LLD')
        
        template_item = template.appendChild(dom.createElement('items')).appendChild(dom.createElement('item'))
        dict_item = {'name':'IPMI Discovery', 'type' : 'IPMI', 'key': 'ipmi.get', 'history' : '2h', 'value_type' : 'TEXT'}
        for i in dict_item:
            template_item.appendChild(dom.createElement(i)).appendChild(dom.createTextNode(dict_item[i]))
        template_item.appendChild(dom.createElement('applications')).appendChild(dom.createElement('application')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI_LLD'))
        lld_macro_dict = {'{#READING_TYPE}':'$.reading.type', 
            '{#SENSOR_ID}':'$.id',
            '{#SENSOR_NAME}':'$.name',
            '{#SENSOR_TYPE_STR}':'$.sensor.text',
            '{#SENSOR_TYPE}':'$.sensor.type',
            '{#SENSOR_UNIT}':'$.units',
            '{#THRESH_HIGH_AVG}':'$.threshold.upper.crit',
            '{#THRESH_HIGH_CRIT}':'$.threshold.upper.non_recover',
            '{#THRESH_HIGH_WARN}':'$.threshold.upper.non_crit',
            '{#THRESH_LOW_AVG}':'$.threshold.lower.crit',
            '{#THRESH_LOW_CRIT}':'$.threshold.lower.non_recover',
            '{#THRESH_LOW_WARN}':'$.threshold.lower.non_crit',
            '{#STATE_TEXT}':'$.state.text'
           }
        
        sensor_chinese = pd.read_json('./sensor.json',orient = 'index')
        sensor_chinese = sensor_chinese.to_dict(orient = 'list')
        
        template_discovery = template.appendChild(dom.createElement('discovery_rules'))
        for application in applications:
            discovery_rule = template_discovery.appendChild(dom.createElement('discovery_rule'))
            discovery_rule.appendChild(dom.createElement('name')).appendChild(dom.createTextNode('IPMI Discovery: {}'.format(' '.join([i.capitalize() for i in application.split('_')]))))
            discovery_rule.appendChild(dom.createElement('type')).appendChild(dom.createTextNode('DEPENDENT'))
            discovery_rule.appendChild(dom.createElement('key')).appendChild(dom.createTextNode('ipmi.sensor.discovery.{}'.format(application)))
            discovery_rule.appendChild(dom.createElement('delay')).appendChild(dom.createTextNode('0'))
            discovery_rule.appendChild(dom.createElement('lifetime')).appendChild(dom.createTextNode('7d'))
            discovery_rule.appendChild(dom.createElement('master_item')).appendChild(dom.createElement('key')).appendChild(dom.createTextNode('ipmi.get'))

            rule_filter = discovery_rule.appendChild(dom.createElement('filter')).appendChild(dom.createElement('conditions'))
            filter_condition = rule_filter.appendChild(dom.createElement('condition'))
            filter_condition.appendChild(dom.createElement('macro')).appendChild(dom.createTextNode('{#SENSOR_TYPE}'))
            value_sensor = '^{}$'.format(str(list(set([i['type'] for i in data[data['sensor'].apply(lambda x: x['text'] == application)]['sensor']]))[0]))
            filter_condition.appendChild(dom.createElement('value')).appendChild(dom.createTextNode(value_sensor))
            filter_condition.appendChild(dom.createElement('formulaid')).appendChild(dom.createTextNode('B'))

            filter_condition = rule_filter.appendChild(dom.createElement('condition'))
            filter_condition.appendChild(dom.createElement('macro')).appendChild(dom.createTextNode('{#READING_TYPE}'))
            reading = list(set([i['type'] for i in data[data['sensor'].apply(lambda x: x['text'] == application)]['reading']]))
            if len(reading) == 1:
                value_sensor = '^{}$'.format(reading[0])
            else:
                value_sensor = '^({})$'.format('|'.join([str(i) for i in reading]))
            filter_condition.appendChild(dom.createElement('value')).appendChild(dom.createTextNode(value_sensor))
            filter_condition.appendChild(dom.createElement('formulaid')).appendChild(dom.createTextNode('A'))
            item_prototypes = discovery_rule.appendChild(dom.createElement('item_prototypes'))
            item_prototype = item_prototypes.appendChild(dom.createElement('item_prototype'))
            sensor = data[data['reading'].apply(lambda x : x['text'] == 'threshold')]['sensor']

            application_chinese = [sensor_chinese[i][0] for i in sensor_chinese if application == i]
            if application_chinese:
                state_description = application_chinese[0]+'传感器ID: {#SENSOR_ID}'+application_chinese[0]+'传感器名字: {#SENSOR_NAME}'+application_chinese[0]+'传感器状态: {#STATE_TEXT}'
                threshold_description = application_chinese[0]+'传感器ID: {#SENSOR_ID}\n' + application_chinese[0] +'传感器名字: {#SENSOR_NAME}\n' + application_chinese[0]+'传感器阈值\n'+'严重告警: {#THRESH_HIGH_WARN} , {#THRESH_HIGH_AVG} , {#THRESH_HIGH_CRIT} \n轻微告警: {#THRESH_LOW_WARN} , {#THRESH_LOW_AVG} , {#THRESH_LOW_CRIT}'
            else:
                application_chinese = [' ']
                state_description = application_chinese[0]+'传感器ID: {#SENSOR_ID}'+application_chinese[0]+'传感器名字: {#SENSOR_NAME}'+application_chinese[0]+'传感器状态: {#STATE_TEXT}'
                threshold_description = application_chinese[0]+'传感器ID: {#SENSOR_ID}\n' + application_chinese[0] +'传感器名字: {#SENSOR_NAME}\n' + application_chinese[0]+'传感器阈值\n'+'严重告警: {#THRESH_HIGH_WARN} , {#THRESH_HIGH_AVG} , {#THRESH_HIGH_CRIT} \n轻微告警: {#THRESH_LOW_WARN} , {#THRESH_LOW_AVG} , {#THRESH_LOW_CRIT}'

            preprocessing = item_prototype.appendChild(dom.createElement('preprocessing')).appendChild(dom.createElement('step'))
            preprocessing.appendChild(dom.createElement('type')).appendChild(dom.createTextNode('JSONPATH'))
            item_prototype.appendChild(dom.createElement('name')).appendChild(dom.createTextNode(application_chinese[0] + '传感器: {#SENSOR_ID}的当前状态值'))
            item_prototype.appendChild(dom.createElement('description')).appendChild(dom.createTextNode(state_description))
            preprocessing.appendChild(dom.createElement('params')).appendChild(dom.createTextNode("$.[?(@.id=='{#SENSOR_ID}')].state.state.first()"))        
            item_prototype.appendChild(dom.createElement('type')).appendChild(dom.createTextNode('DEPENDENT'))
            item_prototype.appendChild(dom.createElement('key')).appendChild(dom.createTextNode('ipmi.sensor.'+ application +'[{#SENSOR_ID}]'))
            item_prototype.appendChild(dom.createElement('delay')).appendChild(dom.createTextNode('0'))
            item_prototype.appendChild(dom.createElement('history')).appendChild(dom.createTextNode('7d'))
            item_prototype.appendChild(dom.createElement('applications')).appendChild(dom.createElement('application')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode(application))
            item_prototype.appendChild(dom.createElement('master_item')).appendChild(dom.createElement('key')).appendChild(dom.createTextNode('ipmi.get'))

            if application in [i['text'] for i in sensor]:
                item_prototype = item_prototypes.appendChild(dom.createElement('item_prototype'))
                item_prototype.appendChild(dom.createElement('name')).appendChild(dom.createTextNode(application_chinese[0] + '传感器: {#SENSOR_ID}的当前值'))
                item_prototype.appendChild(dom.createElement('description')).appendChild(dom.createTextNode(threshold_description))
                if application == 'temperature':
                    item_prototype.appendChild(dom.createElement('units')).appendChild(dom.createTextNode('℃')) 
                else:
                    units = list(set(data[data['sensor'].apply(lambda x :x['text'] == application)]['units']))[0]
                    item_prototype.appendChild(dom.createElement('units')).appendChild(dom.createTextNode(units))  
                preprocessing = item_prototype.appendChild(dom.createElement('preprocessing')).appendChild(dom.createElement('step'))
                preprocessing.appendChild(dom.createElement('type')).appendChild(dom.createTextNode('JSONPATH'))
                preprocessing.appendChild(dom.createElement('params')).appendChild(dom.createTextNode("$.[?(@.id=='{#SENSOR_ID}')].value.first()"))
                item_prototype.appendChild(dom.createElement('type')).appendChild(dom.createTextNode('DEPENDENT'))
                item_prototype.appendChild(dom.createElement('key')).appendChild(dom.createTextNode('ipmi.sensor.'+ application +'.value.[{#SENSOR_ID}]'))
                item_prototype.appendChild(dom.createElement('delay')).appendChild(dom.createTextNode('0'))
                item_prototype.appendChild(dom.createElement('history')).appendChild(dom.createTextNode('7d'))
                item_prototype.appendChild(dom.createElement('applications')).appendChild(dom.createElement('application')).appendChild(dom.createElement('name')).appendChild(dom.createTextNode(application))
                item_prototype.appendChild(dom.createElement('master_item')).appendChild(dom.createElement('key')).appendChild(dom.createTextNode('ipmi.get'))


            lld_macros = discovery_rule.appendChild(dom.createElement('lld_macro_paths'))
            for macro in lld_macro_dict:
                lld_macro = lld_macros.appendChild(dom.createElement('lld_macro_path'))
                lld_macro.appendChild(dom.createElement('lld_macro')).appendChild(dom.createTextNode(macro))
                lld_macro.appendChild(dom.createElement('path')).appendChild(dom.createTextNode(lld_macro_dict[macro]))

        try:
            with open(self.save_path + self.json_file.split('/')[-1].split('.json')[0]+'.xml','w',encoding = 'UTF-8') as fh:
                dom.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
                #print('写入xml OK!')
        except Exception as err:
            print('错误信息：{0}'.format(err))
                
        
if __name__ == '__main__':
    json_file = './host_json/10495_192.168.50.20.json'
    ct = Create_Template(json_file)
    ct.create_xml()
