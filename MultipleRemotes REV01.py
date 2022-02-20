import time
import serial
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse
from pymodbus.register_write_message import WriteSingleRegisterRequest
from configparser import ConfigParser

global client_rtu
global rtu_indicator

# Config file handler.
config_parser = ConfigParser()
configFilePath = 'D:\\NEW\\Projects\\Precia Molen Australia\\Multiple Remotes\\config.ini'
config_parser.read(configFilePath)
# PreciaIndicator  parameters.
rtu_port =  config_parser.get('PreciaIndicator', 'rtu_port') 
rtu_stopbits = int(config_parser.get('PreciaIndicator', 'rtu_stopbits'))
rtu_bytesize = int(config_parser.get('PreciaIndicator', 'rtu_bytesize'))
rtu_parity = config_parser.get('PreciaIndicator', 'rtu_parity')
rtu_baudrate = int(config_parser.get('PreciaIndicator', 'rtu_baudrate'))
rtu_address = int(config_parser.get('PreciaIndicator', 'rtu_address'))
number_of_channels = int(config_parser.get('PreciaIndicator', 'number_of_channels'))
scale_unit = config_parser.get('PreciaIndicator', 'scale_unit')
# RemoteDisplay parameters.
remote_baudrate = int(config_parser.get('RemoteDisplay', 'remote_baudrate'))
remote_port = [config_parser.get('RemoteDisplay','channel01_port'), config_parser.get('RemoteDisplay','channel02_port'), config_parser.get('RemoteDisplay','channel03_port'), 
config_parser.get('RemoteDisplay','channel04_port'), config_parser.get('RemoteDisplay','channel05_port'), config_parser.get('RemoteDisplay','channel06_port') , config_parser.get('RemoteDisplay','channel07_port'), 
config_parser.get('RemoteDisplay','channel08_port'), config_parser.get('RemoteDisplay','channel09_port'), config_parser.get('RemoteDisplay','channel10_port')]

# RTU setup and connection.
client_rtu = ModbusClient(method='rtu', port=rtu_port, stopbits=rtu_stopbits, bytesize=rtu_bytesize, parity=rtu_parity, baudrate=rtu_baudrate, timeout1=0.050)
connection = client_rtu.connect()
print (connection)
# Net value for Channel 1~10
rtu_indicator = [260+rtu_address, 270+rtu_address, 280+rtu_address, 290+rtu_address, 300+rtu_address, 310+rtu_address, 320+rtu_address, 330+rtu_address, 340+rtu_address, 350+rtu_address]

# Serial setup for each remote display.
ser_dictionary = {}
for x in range(number_of_channels):
	ser_dictionary["ser%s" %x] = serial.Serial(remote_port[x], remote_baudrate, timeout=0.050)

# Mimic Master A+ protocol and transmit over the serial assignment for the channel.
def remote(weight,display):
	weight = weight.replace("[","").replace("]","")
	weight = weight.zfill(6)
	msg = "\x01\x0901\x02040200\x0201" + weight + ".kg\x0202000000.kg\x0203" + weight + ".kg\r\n"
	ser_dictionary["ser%s" %display].write(msg.encode())

# Loop for the RTU and execute transmission (200 ms)
try:
    while True:
    	display = [client_rtu.read_input_registers(rtu_indicator[0], unit=0x01), client_rtu.read_input_registers(rtu_indicator[1], unit=0x01), 
    	client_rtu.read_input_registers(rtu_indicator[2], unit=0x01), client_rtu.read_input_registers(rtu_indicator[3], unit=0x01), 
    	client_rtu.read_input_registers(rtu_indicator[4], unit=0x01), client_rtu.read_input_registers(rtu_indicator[5], unit=0x01), 
    	client_rtu.read_input_registers(rtu_indicator[6], unit=0x01), client_rtu.read_input_registers(rtu_indicator[7], unit=0x01),
    	client_rtu.read_input_registers(rtu_indicator[8], unit=0x01), client_rtu.read_input_registers(rtu_indicator[9], unit=0x01)]
    	for x in range(number_of_channels):
    		print(display[x].registers)
    		remote((str(display[x].registers)),x)
    	time.sleep(0.2)

except KeyboardInterrupt:
    print('interrupted!')

"""
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  
     |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||      
        |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||         
          |||||||||||||||                           ||||||||||||||||            
             |||||||||||||||                    |||||||||||||||||               
               |||||||||||||||               ||||||||||||||||                   
                  |||||||||||||||         ||||||||||||||||                      
                     ||||||||||||||    ||||||||||||||||                         
WbIoT                  |||||||||||||||||||||||||||||                            
Precia Molen NZ LTD     |||||||||||||||||||||||                               
Marco DE OLIVEIRA          ||||||||||||||||||                                  
2022                           |||||||||||                                      
                                 ||||||                                         
"""