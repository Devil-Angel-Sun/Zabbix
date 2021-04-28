from pyzabbix import ZabbixAPI
import sched, time, os, push_template,json
import pandas as pd
# zapi = ZabbixAPI('http://192.168.50.100:18080')
# zapi.login('Admin','zabbix')

class Get_message():
    '''
    主要用途：用于将ipmi.get的模板与IPMI的主机相连接，并获取主机的IPMI数据，保存到host_json文件夹下，最后取消模板链接
    参数：excel_path: 需要安装的IPMI表格
         html:zabbix的网址
         user:zabbix的登录用户
         password: zabbix的登录密码
         save_json:ipmi保存的路径
    '''
    
    def __init__(self, excel_path, html, user = 'Admin', password = 'zabbix', save_json = './host_json/'):
        self.excel_path = excel_path
        self.html = html
        self.user = user
        self.password = password
        self.save_json =save_json
        
    def login(self):
        zapi = ZabbixAPI(self.html)
        zapi.login(self.user, self.password)
        return zapi
    
    def get_data(self):
        '''获取需要安装的IPMI的表格'''
        data = pd.read_excel(self.excel_path)
        return data
    
    def get_hosts_id(self):
        '''获取所有主机的hostid和host信息,并取出所需主机的hostid和host'''
        zapi = self.login()
        data = self.get_data()
        host_list = zapi.host.get(output = ['hostid', 'host'])
        host_dict = {}
        for i in host_list:
            if i['host'] in list(data['host']):
                host_dict[i['hostid']] = i['host']
        return host_dict
    
    def get_template_id(self):
        '''获取所有模板的id和名字信息,并取出所需模板的templateid'''
        zapi = self.login()
        template_list = zapi.template.get(output=["templateid","name"])
        return int([i['templateid'] for i in template_list if i['name'] == 'Template ipmi_get of IPMI'][0])
    
    def link_template(self, host):
        zapi = self.login()
        add_template = zapi.template.massadd(templates = self.get_template_id(), hosts={"hostid": host})
            
    def push_host(self):
        '''将ipmi.get的模板添加到所需主机上'''
        host_dict = self.get_hosts_id()        
        for host in host_dict:
            self.link_template(host)
            
    def func(self, delay_time):
        print('延迟运行{}分钟'.format(delay_time))
        
    def delay(self):
        '''延时装置：延迟2分钟取数据'''
        print('当前时刻：{}'.format(time.time()))
        s = sched.scheduler(time.time,time.sleep)
        # 2为延后时间，1为优先级，func为函数名，("test1",)为函数参数
        s.enter(120,0,self.func,("2 minute",))
        s.run()
    
    def del_template(self):
        zapi = self.login()
        host_dict = self.get_hosts_id()
        templateid = self.get_template_id()
        for host in host_dict:
            del_template = zapi.host.update(hostid = host, templates_clear = {"templateid": templateid})

    def get_value(self):
        zapi = self.login()
        self.delay()
        host_dict = self.get_hosts_id()
        print(host_dict)
        for host in host_dict:
            item_list = zapi.item.get(hostids = host, search = {"key_" : 'ipmi.get'}, output = "extend")
            try:
                new_data = pd.DataFrame(json.loads(item_list[0]['lastvalue']))
                new_data.to_json(os.path.join(self.save_json, host+'_'+host_dict[host]+'.json'))
            except Exception as err:
                print('错误信息： ' + host_dict[host] + '获取不到ipmi信息')
        self.del_template()
        
if __name__ == '__main__':
    excel_path = './host.xlsx'
    gm = Get_message(excel_path = excel_path)
    gm.push_host()
    gm.get_value()