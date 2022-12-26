#
#    Copyright (c) 2012 Tom Keffer <tke...@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
#    $Revision: 1 $
#    $Author: pobrien $
#    $Date: 2016-01-14 08:00:00 -0500 (Thu, 14 Jan 2016) $
#
#    Wetterdaten von Meteohub Port 5558 abfragen
#
#    Meteohub liefert mit oeffnen des Ports 5558 alle aktuellen Daten und schliesst die Verbindung sofort.
#

import socket
import syslog
import time
import datetime

import weedb
import weewx.drivers
import weeutil.weeutil
import weewx.wxformulas

# weewx4 logging
import weeutil.logger
import logging

log = logging.getLogger(__name__)

def logmsg(dst, msg):
    log.info(msg)

def loginf(msg):
    log.info(msg)

def logerror(msg):
    log.error(msg)

def logdebug(msg):
    log.debug(msg)


def loader(config_dict, engine):
    station = Meteohub(**config_dict['Meteohub'])
    return station

class Meteohub(weewx.drivers.AbstractDevice):
    """ Driver for the Meteohub station. """

    def __init__(self, **stn_dict) :
        """ Initialize an object of type Meteohub. """

        self.host_ip          = stn_dict.get('host_ip')
        self.host_port        = int(stn_dict.get('host_port'))
        self.timeout          = float(stn_dict.get('timeout'))
        self.station_hardware = stn_dict.get('hardware')
        
        self.lastrain = None
        
        self.port = None
        self.openPort()

    def hardware_name(self):
        return self.station_hardware

    def openPort(self):
        # Hier passiert nichts.
        x = 0

    def closePort(self):
#        loginf("closePort [1]")
        self.port.close()
        self.socket.close()

    def check_rain(self, rain_counter):
        # *** DO NOT use the &rainin= data! ***
        # Handle the rain accum by taking the &dailyrainin= reading ONLY.
        # Then submit those minor increments of daily rain to weewx.
        rain = 0.0
        current_rain = rain_counter
        if self.lastrain is not None:
            if (current_rain >= self.lastrain):
                rain = float(current_rain) - float(self.lastrain)
        self.lastrain = current_rain
        return rain
        
    def mhsleep(self,ts):
        # Sleep for the time 'ts' [s]
        t1 = datetime.datetime.now()
        while True:
            time.sleep(1)
            t2 = datetime.datetime.now()
            d = t2 - t1
            if d.seconds > ts:
                return

    #===============================================================================
    #                         LOOP record decoding functions
    #===============================================================================

    def genLoopPackets(self):
        """ Generator function that continuously returns loop packets """
        
        while True:
          self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          try:
            self.socket.connect((self.host_ip,self.host_port))
            error = False
          except:
            error = True
          if error == True:
            self.socket.close()
            logerror("socket.connect FAILED ! host %s on port %d" % (self.host_ip,self.host_port))
            time.sleep(10)
            continue 
#          logdebug("socket.connect ok ! host %s on port %d" % (self.host_ip,self.host_port))
          self.port = self.socket.makefile(mode='rb')
          
          _packet = {}
          _packet['usUnits'] = weewx.METRICWX
          run = True
          while run == True:
            _line = self.port.readline()
            
            if len(_line) == 0:
#              logdebug(" => done !" )
              break                                       # Ende erreicht -> Schleife verlassen und neue Verbindung aufbauen
            elif (_line == b'') or (_line is None):
              x = 0
            else:
              try:
                s1 = _line.decode()
                
                if s1.find('actual_utcdate ') >= 0:
                  # Beispiel: 20221218150212
                  list = s1.split(' ')
                  dt = datetime.datetime.strptime(str(int(list[1])) + " +0000",'%Y%m%d%H%M%S %z')
                  ts = datetime.datetime.timestamp(dt)
                  _packet['dateTime'] = int(ts)
#                  logdebug("actual_utcdate = " + str(_packet['dateTime']))

                elif s1.find('actual_th0_temp_c') >= 0:
                  # Beispiel: actual_th0_temp_c -2.4
                  list = s1.split(' ')
                  _packet['outTemp'] = float(list[1])
#                  logdebug("actual_th0_temp_c = " + str(_packet['outTemp']))
                
                elif s1.find('actual_th0_hum_rel') >= 0:
                  # Beispiel: actual_th0_hum_rel 87
                  list = s1.split(' ')
                  _packet['outHumidity'] = float(list[1])
#                  logdebug("actual_th0_hum_rel = " + str(_packet['outHumidity']))

                elif s1.find('actual_thb0_temp_c') >= 0:
                  # Beispiel: actual_thb0_temp_c 22.3
                  list = s1.split(' ')
                  _packet['inTemp'] = float(list[1])
#                  logdebug("actual_thb0_temp_c = " + str(_packet['inTemp']))

                elif s1.find('actual_thb0_hum_rel') >= 0:
                  # Beispiel: actual_thb0_hum_rel 34
                  list = s1.split(' ')
                  _packet['inHumidity'] = float(list[1])
#                  logdebug("actual_thb0_temp_c = " + str(_packet['inHumidity']))

                elif s1.find('actual_thb0_sealevel_hpa') >= 0:
                  # Beispiel: actual_thb0_sealevel_hpa 1027.4
                  list = s1.split(' ')
                  _packet['barometer'] = float(list[1])
#                  logdebug("actual_thb0_sealevel_hpa = " + str(_packet['barometer']))


                elif s1.find('actual_th10_temp_c') >= 0:                                           # th10 - Temperatur
                  # Beispiel: actual_th10_temp_c 0.0
                  list = s1.split(' ')
                  _packet['leafTemp1'] = float(list[1])
#                  logdebug("actual_th10_temp_c = " + str(_packet['leafTemp1']))

                elif s1.find('actual_th10_hum_rel') >= 0:                                          # th10 - Blattfeuchte
                  # Beispiel: actual_th10_hum_rel 2
                  list = s1.split(' ')
                  _packet['leafWet1'] = float(list[1])
#                  logdebug("actual_th10_hum_rel = " + str(_packet['leafWet1']))


                elif s1.find('actual_th13_temp_c') >= 0:                                           # th13 - Bodentemperatur
                  # Beispiel: actual_th13_temp_c 2.2
                  list = s1.split(' ')
                  _packet['soilTemp2'] = float(list[1])
#                  logdebug("actual_th13_temp_c = " + str(_packet['soilTemp2']))


                elif s1.find('actual_th20_temp_c') >= 0:                                           # th20 - Bodentemperatur (wie th13)
                  # Beispiel: actual_th20_temp_c 2.2
                  list = s1.split(' ')
                  _packet['soilTemp2'] = float(list[1])
#                  logdebug("actual_th20_temp_c = " + str(_packet['soilTemp2']))

                elif s1.find('actual_th20_hum_rel') >= 0:                                          # th20 - Bodenfeuchte
                  # Beispiel: actual_th20_hum_rel 35
                  list = s1.split(' ')
                  _packet['soilMoist2'] = float(list[1])
#                  logdebug("actual_th20_hum_rel = " + str(_packet['soilMoist2']))


                elif s1.find('actual_sol0_radiation_wqm') >= 0:
                  # Beispiel: actual_sol0_radiation_wqm 16.0
                  list = s1.split(' ')
                  _packet['radiation'] = float(list[1])
#                  logdebug("actual_sol0_radiation_wqm = " + str(_packet['radiation']))

                elif s1.find('actual_uv0_index') >= 0:
                  # Beispiel: actual_uv0_index 0.0
                  list = s1.split(' ')
                  _packet['UV'] = float(list[1])
#                  logdebug("actual_uv0_index = " + str(_packet['UV']))

                elif s1.find('actual_wind0_dir_deg') >= 0:
                  # Beispiel: actual_wind0_dir_deg 240
                  list = s1.split(' ')
                  _packet['windDir'] = float(list[1])
#                  logdebug("actual_wind0_dir_deg = " + str(_packet['windDir']))

                elif s1.find('actual_wind0_speed_ms') >= 0:
                  # Beispiel: actual_wind0_speed_ms 0.0
                  list = s1.split(' ')
                  _packet['windSpeed'] = float(list[1])
#                  logdebug("actual_wind0_speed_ms = " + str(_packet['windSpeed']))

                elif s1.find('actual_wind0_gustspeed_ms') >= 0:
                  # Beispiel: actual_wind0_gustspeed_ms 0.0
                  list = s1.split(' ')
                  _packet['windGust'] = float(list[1])
#                  logdebug("actual_wind0_gustspeed_ms = " + str(_packet['windGust']))

                elif s1.find('actual_rain0_total_mm') >= 0:
                  # Beispiel: actual_rain0_total_mm 767.0
                  list = s1.split(' ')
                  rain = self.check_rain(float(list[1]))
                  _packet['rain'] = rain
#                  logdebug("actual_rain0_total_mm = " + str(_packet['rain']))

              except:
                x = 0
          
          if len(_packet) > 2:
            logdebug(_packet)
            yield _packet
          
          self.port.close()
          self.socket.close()
          
          time.sleep(30)
                        
# --------------------------------------------------------------------------------------------------------
