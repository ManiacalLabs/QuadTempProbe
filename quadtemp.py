#QuadTempProbe
#by Dan, of ManiacalLabs.com

#https://github.com/timofurrer/ds18b20
from ds18b20 import DS18B20
#*************************************

#https://github.com/matze/python-phant
import phant
#*************************************


import datetime
import smtplib

#***USER CONFIG****
#Alarm Enable (set to '= 1' to enable alarm)
ALARM_SENSOR1 = 0
ALARM_SENSOR2 = 0
ALARM_SENSOR3 = 0
ALARM_SENSOR4 = 0

#Alarm Threshold (if sensor reads higher than this (degrees F), trigger alert)
SENSOR1_ALERT = -10
SENSOR2_ALERT = 40
SENSOR3_ALERT = 40
SENSOR4_ALERT = 10
#******************

#Credit to https://github.com/matze/python-phant for phant (used on data.sparkfun.com) library
p = phant.Phant('*PUBLICKEY', 'sensor1', 'sensor2', 'sensor3', 'sensor4', 'temp1', 'temp2', 'temp3', 'temp4', private_key='*PRIVATEKEY*')


#NOTE: see the example script in the DS18B20 library to find the IDs for your sensors
sensor1= DS18B20("000005e81979")
sensor2= DS18B20("000005e893a1")
sensor3= DS18B20("000005e89e0e")
sensor4= DS18B20("000005e7e753")

sensor1_temp = sensor1.get_temperature(DS18B20.DEGREES_F)
sensor2_temp = sensor2.get_temperature(DS18B20.DEGREES_F)
sensor3_temp = sensor3.get_temperature(DS18B20.DEGREES_F)
sensor4_temp = sensor4.get_temperature(DS18B20.DEGREES_F)

#Credit to this article for the gmail method:
#http://computers.tutsplus.com/tutorials/build-a-raspberry-pi-moisture-sensor-to-monitor-your-plants--mac-52875
def send_gmail(from_name, sender, password, recipient, subject, body):
    '''Send an email using a GMail account.'''
    senddate=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    msg="Date: %s\r\nFrom: %s <%s>\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (senddate, from_name, sender, recipient, subject)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, recipient, msg+body)
    server.quit()

#Send to data.sparkfun.com stream
p.log(sensor1.get_id(), sensor2.get_id(), sensor3.get_id(), sensor4.get_id(), sensor1_temp, sensor2_temp, sensor3_temp, sensor4_temp)

if ALARM_SENSOR1:
    if sensor1_temp >= SENSOR1_ALERT:
        send_gmail('*SENDERNAME*', '*SENDEREMAIL*@gmail.com', '*SENDEREMAILPASSWORD*', '*RECIPIENTEMAIL*@domain.com', 'ALERT SENSOR 1', 'SENSOR 1 TEMP: %s' % sensor1_temp)

if ALARM_SENSOR2:
    if sensor2_temp >= SENSOR2_ALERT:
        send_gmail('*SENDERNAME*', '*SENDEREMAIL*@gmail.com', '*SENDEREMAILPASSWORD*', '*RECIPIENTEMAIL*@domain.com', 'ALERT SENSOR 2', 'SENSOR 2 TEMP: %s' % sensor2_temp)

if ALARM_SENSOR3:
    if sensor3_temp >= SENSOR3_ALERT:
        send_gmail('*SENDERNAME*', '*SENDEREMAIL*@gmail.com', '*SENDEREMAILPASSWORD*', '*RECIPIENTEMAIL*@domain.com', 'ALERT SENSOR 3', 'SENSOR 3 TEMP: %s' % sensor3_temp)

if ALARM_SENSOR4:
    if sensor4_temp >= SENSOR4_ALERT:
        send_gmail('*SENDERNAME*', '*SENDEREMAIL*@gmail.com', '*SENDEREMAILPASSWORD*', '*RECIPIENTEMAIL*@domain.com', 'ALERT SENSOR 4', 'SENSOR 4 TEMP: %s' % sensor4_temp)
