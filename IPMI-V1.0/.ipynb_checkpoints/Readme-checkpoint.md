step 1： 运行create_host.py和create_ipmi.py
step 2： 运行push_template.py，将host和ipmi模板推送到zabbix
step 3： 运行get_information.py，将ipmi模板连接到host中，并取得ipmi.get数据，最后删除模板
step 4： 运行create_template.py,将用ipmi.get获取的数据生成模板
step 5： 运行push_template.py，将所有模板都推送到zabbix上
step 6： 运行link_template，将最终模板链接到响应的host上
注意：sensor.py 一般不用，除非有新的类型出现