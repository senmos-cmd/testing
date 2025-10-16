from tcp_modbus_class import Modbus;

sensor = '1921-003-0013'   
mdb_obj = Modbus(sensor)
os=mdb_obj.get_sensor_OS()