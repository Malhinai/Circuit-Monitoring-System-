#print(open('./main.py','rU').read())

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import BME280
from machine import Pin, I2C

import gc
gc.collect()

ssid = 'TP-Link_1C4A'
password = '12345678'
mqtt_server = '192.168.0.101'

client_id = ubinascii.hexlify(machine.unique_id())

topic_pub_temp = b'esp/bme280/temperature'
topic_pub_hum = b'esp/bme280/humidity'
topic_pub_pres = b'esp/bme280/pressure'
topic_pub_fanstate=b'esp/bme280/fanstate'
topic_pub_liquid=b'esp/bme280/liquid'

last_message = 0
message_interval = 0.15

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)


while station.isconnected() == False:
  pass

print('Connection successful')

# ESP32 - Pin assignment
#i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
# ESP8266 - Pin assignment
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)
bme = BME280.BME280(i2c=i2c)
relay=Pin(15,Pin.OUT)
buzzer=Pin(14,Pin.OUT)

def connect_mqtt():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  #client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def read_bme_sensor():
  try:
    temp = b'%s' % bme.temperature[:-1]
    #temp = (b'{0:3.1f},'.format((bme.read_temperature()/100) * (9/5) + 32))
    hum = b'%s' % bme.humidity[:-1]

    pres = b'%s'% bme.pressure[:-3]

    return temp, hum, pres
    #else:
    #  return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    if (time.time() - last_message) > message_interval:
      temp, hum, pres = read_bme_sensor()
      #floatemp=float_from_bytes(str(temp))
      floatemp=float(temp.decode("utf8",'strict'))
      floathum=float(hum.decode("utf8",'strict'))
      print(temp)
      print(floatemp)
      if(floatemp> float(30) ):
        relay.value(1)
        buzzer.value(1)
        client.publish(topic_pub_fanstate, b'warning!: the cooling fan is on the temperature is above normal')
      elif (floatemp< float(30) ):
        relay.value(0)
        buzzer.value(0)
        client.publish(topic_pub_fanstate, b'the cooling fan is off the tempreture is average')
      print(hum)
      print(pres)
      client.publish(topic_pub_temp, temp)
      client.publish(topic_pub_hum, hum)      
      client.publish(topic_pub_pres, pres)
      
      if (floathum>float(50)):
        client.publish(topic_pub_liquid,b'warning!: there might be a water spillage')
      elif (floathum<float(50)):
        client.publish(topic_pub_liquid,b'the humidity level is average')

      last_message = time.time()
  except OSError as e:
    restart_and_reconnect()

