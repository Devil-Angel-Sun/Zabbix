import pandas as pd

class Add_Sensor:
    '''
    使用场景：如果存在新的类型或者需要修改已有类型的含义，那么启用该函数；否则用已存在的sensor.json即可
    参数：sensor_key:需要加入新类型的name,往往存在于IPMI的get信息中
        sensor_value:新类型的中文释义，用于生成在最终模板的描述性语句中
        save_file:保存文件的路径，默认情况下为当前路径下，即覆盖已存在的sensor.json文件
    '''
    def __init__(self, sensor_key, sensor_value, save_file = './sensor.json'):
        self.sensor_key = sensor_key
        self.sensor_value = sensor_value
        self.save_file = save_file
        
    def add(self):
        sensor = {'add_in_card': '附加卡',
         'battery': '电池',
         'boot_error': '启动错误',
          'button':'按钮',
          'cable_interconnect':' 电缆/互连',
          'critical_interrupt':'紧急中断',
          'chip_set':'芯片组',
          'cooling_device':'冷却设备',
          'drive_slot':'驱动器插糟/托架',
          'event_logging_disabled':'已禁用事件日志',
          'entity_presence':'实体',
          'fan': '风扇',
          'fan_status':'风扇',
          'management_subsystem_health':'子系统健康',
          'memory':'内存',
          'microcontroller_coprocessor':' 微控制器/微处理器',
          'module_board':'模块/电路板',
          'other_units_based_sensor':'其他',
          'power_supply':'电源',
          'ps_status':'电源',
          'processor':'处理器',
          'slot_connector':'插槽/连接器',
          'system_acpi_power_state':'',
          'system_boot_initiated':'系统引导启动',
          'system_event':'系统事件日志',
          'system_firmware_progress':'系统固件',
          'temperature':'温度',
          'temperature_status':'温度',
          'terminator':'',
          'voltage':'电压',
          'voltage_state':'电压',
          'watchdog_2':'看门狗',
         'chassis_intru':'物理健康',
          'physical_security': '物理健康'
         }
        sensor[self.sensor_key] = self.sensor_value
        return sensor
    
    def to_json(self):
        sensor = self.add()
        sensor = pd.DataFrame(sensor, index = [0])
        sensor.to_json(self.save_file,orient = 'index')
        
if __name__ == '__main__':
    sensor_key = 'physical_security'
    sensor_value = '物理健康'
    addsensor = Add_Sensor(sensor_key = sensor_key, sensor_value = sensor_value)
    addsensor.to_json()