from tcp_modbus_class import Modbus;

sensor = 'es1-2540-0149' 
mdb_obj = Modbus(sensor)
os=mdb_obj.get_sensor_OS()
print(os)
sn=mdb_obj.get_SN()
print(sn)
rev=mdb_obj.get_sensor_Rev()
print(rev)
sysT=mdb_obj.get_sysTemp()
print(sysT)
exhT=mdb_obj.get_exhTemp()
print(exhT)
mdb_obj.close()