import struct, datetime
# from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client import ModbusTcpClient
# from pyModbusTCP.client import ModbusClient

class Modbus:
    def __init__(self, sensor): 
        self.no_con = False
        print('\nTrying to connect to the board...')
        try:
            self.on_off = False
            # self.tcp_m = ModbusClient(host = 'rubaek', port = 1502, auto_open=True, auto_close=True)
            self.tcp_m = ModbusTcpClient(sensor)
            tcp_m = ModbusTcpClient(sensor)
            # if self.tcp_m.open():
            if self.tcp_m.connect():
                self.no_con = True  
        except:
            print('\nNo modbus-connection to analyser')
            self.no_con = False
            
    def get_coils(self, count):
        if self.no_con:
            return self.tcp_m.read_coils(address=0, count=count)
        
    def get_sysTemp(self):
        try:
            if self.no_con:
                exh_temp = self.tcp_m.read_holding_registers(address=12, count=2)
                return str(round(self.convert2float(exh_temp.registers)[0], 2))
            else:
                return '-1'
        except:
            print('\nCan not read data from the analyzer.')
            return '-1'

    def get_exhTemp(self):
        try:
            if self.no_con:
                exh_temp = self.tcp_m.read_holding_registers(address=14, count=2)
                return str(round(self.convert2float(exh_temp.registers)[0], 2))
            else:
                return '-1'
        except:
            print('\nCan not read data from the analyzer.')
            return '-1'

    def get_state(self):
        try:
            if self.no_con:
                state = self.tcp_m.read_holding_registers(address=16, count=1)
                if state != None:
                    return str(state.registers[0])
                else:
                    return '9'
            else:
                return '9'
        except:
            print('\nCan not read data from the analyzer.')
            return '-1'
        
    def get_exhPres(self):
        try:
            if self.no_con:
                exh_pres = self.tcp_m.read_holding_registers(address=10, count=2)
                return str(round(self.convert2float(exh_pres.registers)[0], 3))
            else:
                return '-1'
        except:
            print('\nCan not read data from the analyzer.')
            return '-1'
            
    def get_sysPres(self):
        try:
            if self.no_con:
                sys_pres = self.tcp_m.read_holding_registers(address=8, count=2)
                return str(round(self.convert2float(sys_pres.registers)[0], 3))
            else:
                return '-1'
        except:
            print('\nCan not read data from the analyzer.')
            return '-1'
        
    def get_conc(self, type):
        try:
            if self.no_con:
                match type:
                    case 'NO':
                        conc = self.tcp_m.read_holding_registers(address=2508, count=2)
                    case 'NO2':
                        conc = self.tcp_m.read_holding_registers(address=2510, count=2)
                    case 'SO2':
                        conc = self.tcp_m.read_holding_registers(address=2502, count=2)
                    case 'NH3':
                        conc = self.tcp_m.read_holding_registers(address=2506, count=2)
                    case 'CO2':
                        conc = self.tcp_m.read_holding_registers(address=2500, count=2)
                    case 'rat_SO2_CO2':
                        conc = self.tcp_m.read_holding_registers(address=2504, count=2)
                return str(round(self.convert2float(conc.registers)[0], 2))
        except:
            print('\nCan not read data from the analyzer.')
            return '-1'      
    
    def get_analyzer_data(self):
        S1=[]
        try:
            if self.no_con:
                items = [datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"), self.get_conc('NO'), self.get_sysPres(), self.get_exhPres(), self.get_sysTemp(), self.get_exhTemp(), self.get_state()]
                for item in items:
                    S1.append(item)
            return(S1)
        except:
            S1 = []
            print('\nCan not read data from the analyzer.')
    
    def get_SN(self):
        if self.no_con:
            sn = self.tcp_m.read_holding_registers(address=1100, count=50)
            return self.convert2char(sn.registers)
        else:
            return 'No_SN'
            
    def get_sensor_Rev(self):
        if self.no_con:
            sensor_Rev = self.tcp_m.read_holding_registers(address=1150, count=50)
            # return (self.convert2char(sensor_Rev.registers))[0:6]
            return (self.convert2char(sensor_Rev.registers))[0:25]
        else:
            return 'No_Revision'
    
    def get_sensor_OS(self):
        if self.no_con:
            sensor_OS = self.tcp_m.read_holding_registers(address=1250, count=50)
            return self.convert2char(sensor_OS.registers)  
        else:
            return 'No_OS'        
      
    def start_calib(self):
         if self.no_con:
             self.tcp_m.write_coil(5, 1)
         else:
             print('\nNo modbus-connection to analyzer')
    
    def set_dark_mode(self):
        if self.no_con:
            self.tcp_m.write_coil(10000, 1)
        else:
            print('\nNo modbus-connection to analyzer')
        
    def set_lamp_mode(self):
        if self.no_con:
            self.tcp_m.write_coil(10001, 5)
        else:
            print('\nNo modbus-connection to analyzer') 
     
    def set_obs_mode(self):
        if self.no_con:
            self.tcp_m.write_coil(10002, 1)
        else:
            print('\nNo modbus-connection to analyzer')    
       
    def start_meas(self, on_off):
        if self.no_con:
            self.on_off = on_off
            #print('Start of measurement is {}'.format(on_off))
            if self.on_off == True:
                self.tcp_m.write_coil(0, 1)
            else:
                self.tcp_m.write_coil(0, 0)
        else:
            print('\nNo modbus-connection to analyzer')   
            
    def read_reg_range(self, start_addr, nmr):
        if self.no_con:
            reg_range = self.tcp_m.read_holding_registers(address=start_addr, count=nmr)
            packed_v_list = list(struct.pack('HH', reg_range.registers[i+1], reg_range.registers[i]) for i in range(0, nmr-1, 2))
            if start_addr == 998 and nmr == 2:
                ret_list = list(struct.unpack('i', packed_v_list[i]) for i in range(0, round(nmr/2)))
            else:
                ret_list = list(struct.unpack('f', packed_v_list[i]) for i in range(0, round(nmr/2)))                
            return ret_list
            # return reg_range
        else:
            print('\nNo modbus-connection to analyzer')
            return []
        
    def set_time(self, no_of_sec):
        if self.no_con:
            tmp_reg = self.tcp_m.read_holding_registers(address=998, count=2)
            print(tmp_reg.registers)
            self.tcp_m.write_registers(address=998, values=[tmp_reg.registers[0], tmp_reg.registers[1] + no_of_sec])
        else:
            print('\nNo modbus-connection to analyzer')
 
 
    def close(self):
        if self.no_con:
            self.tcp_m.close()
        else:
            print('No modbus-connection to analyzer')
            
    def convert2float(self, reg):
        if self.no_con:
            packed_v = struct.pack('HH', reg[1], reg[0])
            return struct.unpack('f', packed_v)
        else:
            return -1
        
    def convert2char(self, list_x):
        list_out = ''
        for reg in list_x:            
            packed_v = struct.pack('H', reg)
            char_first = chr(packed_v[1])
            char_2nd = chr(packed_v[0])
            if (char_first != '\x00'):
                list_out += char_first
            if (char_2nd != '\x00'):
                list_out += char_2nd
        return list_out      
