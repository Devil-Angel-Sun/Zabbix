import glob, argparse
from create_host import Create_host
from create_ipmi import Create_IPMI
from push_template import Push_Template
from get_information import Get_message
from create_template import Create_Template
from link_template import Link_Template


def main(args):
    # 创建host.xml文件
#     excel_path = './host.xlsx'
    ch = Create_host(excel_path = args.excel_path)
    ch.save_host()

    # 创建ipmi.get的xml文件
    ci = Create_IPMI()
    ci.save_ipmi()

    # 推送上述两个文件
#     html = "http://192.168.50.100:18080"
    pt = Push_Template(html = args.html, user = args.user, password = args.password)
    pt.push()

    # 获取主机相关的ipmi信息
    gm = Get_message(excel_path = args.excel_path, html = args.html, user = args.user, password = args.password)
    gm.push_host()
    gm.get_value()

    ## 为每一个host创建单独的模板
    data = glob.glob('./host_json/*.json')
    for i in data:
        ct = Create_Template(i)
        ct.create_xml()

    ## 再次推送所有文件
    pt = Push_Template(html = args.html, user = args.user, password = args.password)
    pt.push()

    ## 链接模板
    lt = Link_Template(excel_path = args.excel_path, html = args.html, user = args.user, password = args.password)
    lt.link()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IPMI Host Link IPMI Template')
    parser.add_argument('--excel_path', default='./host.xlsx', help='Excel of Host')
    parser.add_argument('--html', default='http://192.168.50.100:18080', help='Address of Zabbix')
    parser.add_argument('--user', default = 'Admin', help = 'User of Zabbix')
    parser.add_argument('--password', default = 'zabbix', help = 'Password of Zabbix')
    args = parser.parse_args()
    main(args)