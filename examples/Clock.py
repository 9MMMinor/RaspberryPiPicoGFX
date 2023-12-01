from location import Location

import machine
import network            
import utime as time
try:
    import socket
except:
    import usocket as socket
try:
    import ustruct as struct
except:
    import struct
from machine import Pin, Timer, reset
from math import acos, asin, ceil, cos, degrees as deg, fmod as mod,\
                 sqrt, radians as rad, sin, pi, floor, atan, tan
import uasyncio as asyncio
from network import WLAN
import json, os

from TimesNR39x37 import TimesNR39x37
from FreeMonoBoldOblique24pt7b import FreeMonoBoldOblique24pt7b
from adafruit_gfx import GFX
from machine import Pin, SPI
from TFT_22_ILI9225 import TFT_22_ILI9225
from glcFont import glcFont
from gfxFont import gfxFont


#   ------------------------------------------------------
#   connectWiFi()
#     connect to local WiFi with specific IP address
#   ------------------------------------------------------
def connectWiFi(ssid, pswd):
    wlan = network.WLAN(network.STA_IF)
    # configuration below MUST match your home router settings!!
    # We want specific IP, 192.168.1.50, rather than usual next available
    # pick what works for your network and save in your phone for toggle relay over web
    wlan.active(True)
    wlan.ifconfig(('192.168.1.52', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
    wlan.ifconfig()
    wlan.connect(ssid,  pswd)
    
    max_wait = 10
    while max_wait > 0:
        """
            0   STAT_IDLE -- no connection and no activity,
            1   STAT_CONNECTING -- connecting in progress,
            -3  STAT_WRONG_PASSWORD -- failed due to incorrect password,
            -2  STAT_NO_AP_FOUND -- failed because no access point replied,
            -1  STAT_CONNECT_FAIL -- failed due to other problems,
            3   STAT_GOT_IP -- connection successful.
        """
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
        
    if wlan.status() != 3:
        return wlan.status()
        
    print('WiFi connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    return status

# ----------------------------------
# keepOrChange(prompt_string, value)
#    return input or keep value
# ----------------------------------
def keepOrChange(prompt, value):
    while True:
        yn = input('Keep ' + prompt + ' == ' + str(value) + '? (y/n) >')
        if yn == 'y':
            return value
        elif yn == 'n':
            value = input('Enter new value > ')



# Edit for your location (See location.py):
home = [ 40.8437793, -124.064459, -8, "PST", +1, "PDT"]

SECPERDAY = (60*60*24)
SECPERHOUR = (60*60)
SECPERMIN = (60)
NTP_DELTA = 2208988800
led = Pin("LED", Pin.OUT, value=0)
host = "0.pool.ntp.org"

COLOR_BLUE           = 0x001F      #   0,   0, 255
COLOR_ORANGE         = 0xFD20      # 255, 165,   0
COLOR_BLACK          = 0x0000      #   0,   0,   0


def parse_sec(t):
    day = int( t/SECPERDAY )
    left = int( t%SECPERDAY )
    if left < 0:
        left += SECPERDAY
        day -= 1
    hours = int( left/SECPERHOUR )
    left %= SECPERHOUR
    minutes = int( left/SECPERMIN )
    left %= SECPERMIN
    seconds = int( left )
    return [hours, minutes, seconds]


def force_range(v, max):
    # force v to be >= 0 and < max
    if v < 0:
        return v + max
    elif v >= max:
        return v - max
    return v


#   --------------------------------------
#   set_time() sets the system RTC to UTC.
#   --------------------------------------
def set_time():
    
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    host = "pool.ntp.org"
    
    timeout = False
    addr = socket.getaddrinfo(host, 123)[0][-1]
    print("Socket addr:",addr)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(10)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    except:
        print("Socket Timeout")
        timeout = True
    finally:
        s.close()
    if timeout:
        return False
    val = struct.unpack("!I", msg[40:44])[0]
    tm = time.gmtime(val - NTP_DELTA)       #UTC
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    time.sleep(1)
    return True


def initializeWiFi():
    try:
        os.stat('location.txt')
        fs = True
    except OSError:
        fs= False
    if fs:
        f=open('location.txt')
        l=json.load(f)
        loc_object = Location(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7])
        f.close()
        ssid = l[0]
        passwd = l[1]
    else:
        print("No location.txt file")
        """ create location.txt """
        home[0] = keepOrChange('Latitude',home[0])   
        home[1] = keepOrChange("Longitude" , home[1])
        home[2] = keepOrChange("UTC Offset (hours)", home[2])
        home[3] = keepOrChange("Time Zone", home[3])
        home[4] = keepOrChange("DST offset", home[4])
        home[5] = keepOrChange("DST Zone", home[5])

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    nets = wlan.scan()

    if not fs:
        for i in range(len(nets)):
            ssid = str(nets[i][0],'utf-8')
            passwd = input("Enter password for " + ssid + " > ")
            if len(passwd) > 1:
                break
    myLocation = [ssid, passwd, home[0], home[1], home[2], home[3], home[4], home[5]]
    location_object = Location(ssid, passwd, home[0], home[1], home[2], home[3], home[4], home[5])

    status = connectWiFi(ssid,passwd)

    data_file=open('location.txt', 'w')
    json.dump(myLocation,data_file)
    data_file.close()
    return location_object


def Date_str(Mon, Day, Year):
    if Mon < 10:
        Mon = "0" + str(Mon)
    if Day < 10:
        Day = "0" + str(Day)
    return("{}/{}/{}".format(Mon, Day, Year))


def Day_str(wkd, mo, d):
    Day = day[wkd]
    Month = month[mo]
    D = str(d)
    return ("{a} {b} {c}".format(a=Day,b=Month,c=D))
    
    
def Time_str(Hour, Min):
    if Hour < 10:
        Hour = "0" + str(Hour)
    if Min < 10:
        Min = "0" + str(Min)
    return("{}:{}".format(Hour, Min))


def get_TzInfo(myLocation):
    (ut_offset, Tz) = myLocation.get_LocalOffset()
    ut_offset *= 3600
    if isDst(ut_offset):
        (DST_Offset, Tz) = myLocation.get_DSTOffset()
        ut_offset += DST_Offset*3600
    return [ut_offset, Tz]


#   ----------------------------------------------------------------
#   get_localtime(ut_offset)
#       ut_offset is number of seconds offset from UTC to local zone
#       return local time in 8 tupple format:
#       [ year, mon, mday, hour, min, sec, wkday, yearday ]
#    ----------------------------------------------------------------
def get_localtime(ut_offset):
    utc = time.time()    # number of seconds, as an integer, since the Epoch
    return( time.localtime(utc + ut_offset) )


#   ----------------------------------------------------------------
#   get_UTC()
#       return Universal Coordinated Time time in 7 tupple format:
#       [ year  , mon   , day   , hour  , min   , sec   , "UTC" ]
#    ----------------------------------------------------------------
def get_UTC():
    now = time.localtime()
    return [ now[0], now[1], now[2], now[3], now[4], now[5], "UTC" ]


class Sun:
    """
Source:
    Almanac for Computers, 1990
    published by Nautical Almanac Office
    United States Naval Observatory
    Washington, DC 20392

    Inputs:
        day, month, year:      date of sunrise/sunset
        latitude, longitude:   location for sunrise/sunset
        zenith:                Sun's zenith for sunrise/sunset
        offical      = 90 degrees 50'
        civil        = 96 degrees
        nautical     = 102 degrees
        astronomical = 108 degrees

        NOTE: longitude is positive for East and negative for West
        NOTE: the algorithm assumes the use of a calculator with the
        trig functions in "degree" (rather than "radian") mode. Most
        programming languages assume radian arguments, requiring back
        and forth convertions. The factor is 180/pi. So, for instance,
        the equation RA = atan(0.91764 * tan(L)) would be coded as RA
        = (180/pi)*atan(0.91764 * tan((pi/180)*L)) to give a degree
        answer with a degree input for L.
    """

    def __init__(self, day, month, year, lat, lon):
        self._lat = lat
        self._lon = lon
        self._day = day
        self._month = month
        self._year = year


    def get_sunrise_time(self):
        """
        Calculate the sunrise time for given date.
        :param lat: Latitude
        :param lon: Longitude
        :param date: Reference date. Today if not provided.
        :return: UTC sunrise datetime
        :raises: SunTimeException when there is no sunrise and sunset on given location and date
        """
        ut = self._calc_sun_time(True)
        if ut is None:
            raise SunTimeException('The sun never rises on this location (on the specified date)')
        else:
            return int( ut*3600 )
            


    def get_sunset_time(self):
        """
        Calculate the sunset time for given date.
        :param lat: Latitude
        :param lon: Longitude
        :param date: Reference date. Today if not provided= rtc = machine.RTC() print(rtc.datetime())
        :return: UTC sunset datetime
        :raises: SunTimeException when there is no sunrise and sunset on given location and date.
        """
        ut = self._calc_sun_time(False)
        if ut is None:
            raise SunTimeException('The sun never sets on this location (on the specified date)')
        else:
            return int( ut*3600 )


    def _calc_sun_time(self, isRiseTime=True, zenith=90.833333333):
        """
        Calculate sunrise or sunset date.
        :param date: Reference date
        :param isRiseTime: True if you want to calculate sunrise time.
        :param zenith: Sun reference zenith
        :return: UTC sunset or sunrise hours
        :raises: SunTimeException when there is no sunrise and sunset on given location and date
        """
        # isRiseTime == False, returns sunsetTime
        
        day = self._day
        month = self._month
        year = self._year
      
        TO_RAD = pi / 180.0

        # 1. first calculate the day of the year
        N1 = floor(275 * month / 9)
        N2 = floor((month + 9) / 12)
        N3 = (1 + floor((year - 4 * floor(year / 4) + 2) / 3))
        N = N1 - (N2 * N3) + day - 30

        # 2. convert the longitude to hour value and calculate an approximate time
        lngHour = self._lon / 15

        if isRiseTime:
            t = N + ((6 - lngHour) / 24)
        else:  # sunset
            t = N + ((18 - lngHour) / 24)

        # 3. calculate the Sun's mean anomaly
        M = (0.9856 * t) - 3.289

        # 4. calculate the Sun's true longitude
        L = M + (1.916 * sin(TO_RAD * M)) + (0.020 * sin(TO_RAD * 2 * M)) + 282.634
        L = force_range(L, 360)  # NOTE: L adjusted into the range [0,360)

        # 5a. calculate the Sun's right ascension

        RA = (1 / TO_RAD) * atan(0.91764 * tan(TO_RAD * L))
        RA = force_range(RA, 360)  # NOTE: RA adjusted into the range [0,360)

        # 5b. right ascension value needs to be in the same quadrant as L
        Lquadrant = (floor(L / 90)) * 90
        RAquadrant = (floor(RA / 90)) * 90
        RA = RA + (Lquadrant - RAquadrant)

        # 5c. right ascension value needs to be converted into hours
        RA = RA / 15

        # 6. calculate the Sun's declination
        sinDec = 0.39782 * sin(TO_RAD * L)
        cosDec = cos(asin(sinDec))

        # 7a. calculate the Sun's local hour angle
        cosH = (cos(TO_RAD * zenith) - (sinDec * sin(TO_RAD * self._lat))) / (
                    cosDec * cos(TO_RAD * self._lat))

        if cosH > 1:
            return None  # The sun never rises on this location (on the specified date)
        if cosH < -1:
            return None  # The sun never sets on this location (on the specified date)

        # 7b. finish calculating H and convert into hours

        if isRiseTime:
            H = 360 - (1 / TO_RAD) * acos(cosH)
        else:  # setting
            H = (1 / TO_RAD) * acos(cosH)

        H = H / 15

        # 8. calculate local mean time of rising/setting
        T = H + RA - (0.06571 * t) - 6.622

        # 9. adjust back to UTC
        # 10. return UTC hours
        return (T - lngHour)


#   ------------------------------------------------------------------------
#   isDST  -  figure out if DaylightSavingsTime applies
#
#   Automatic DST calculation: DST is on between 2:00 AM
#       the second Sunday of March and 2:00 AM the first
#       sunday in November
#
#   ------------------------------------------------------------------------
SUNDAY = 6
MARCH = 3
NOVEMBER = 11

def isDst(offset):
    now = get_localtime( offset )
    year = now[0]
    mon = now[1]
    day = now[2]
    hour = now[3]
    mar1_tup = (year, 3, 1, 0,0,0,0,0,0)
    time_sec = time.mktime(mar1_tup)
    obj = time.localtime(time_sec)
    Nov1 = Mar1 = obj[6] + 1         # day_of_week (March 1 and November 1 are equal)
    
    # DST is off during December, January, and February and don't bother before 2006
    if mon == 12 or mon == 1 or mon == 2 or year < 2006: 
        return False
    
    # DST is on from April through October */
    if 3 < mon and mon < 11:
        return True
        
    # DST in March or November
    # Calculate day of the week for March 1   
    if Mar1 == SUNDAY:
        firstDay_DST = 8              # second sunday is 8th */
    else:
        firstDay_DST = 15 - Mar1
  
    # Calculate day of the week for November 1   
    if (Nov1 == SUNDAY):
        lastDay_DST = 1        # first sunday is the 1st
    else:
        lastDay_DST = 8 - Nov1

    # DST is off in March until 2 AM on the second Sunday
    if ( (mon == MARCH) and
            ( (day < firstDay_DST) or ((day == firstDay_DST) and (hour < 2)) ) ):
        return False     
    #   DST is off in November after 2 am on first Sunday
    if ( (mon == NOVEMBER) and
            ( (day > lastDay_DST) or ((day == lastDay_DST) and (hour >= 1)) ) ):
        return False
    return True         # rest of March or 1st part of November


print("Main .....")
try:
    lObject = initializeWiFi()
except KeyboardInterrupt:
    machine.reset()

print('Starting up ...')
a=set_time()
print(a)
(Year,Mon,Day,Hour,Min,Sec,Tz) = get_UTC()

print("Date: ", Date_str(Mon, Day, Year))
print("Time: ", Time_str(Hour, Min), Tz)
    
(ut_offset, Tz) = get_TzInfo(lObject)
now = get_localtime(ut_offset)
Hour = now[3]
Min = now[4]
Day = now[2]
Mon = now[1]
Year= now[0]
    
print(Date_str(Mon,Day,Year), Time_str(Hour,Min), )

spi = SPI(0, baudrate=40000000)
lcd = TFT_22_ILI9225(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))
day = {0: "Mon", 1: "Tue", 2:"Wed", 3:"Thu", 4:"Fri", 5:"Sat",
       6:"Sun"}
month = {0: "Jan", 1: "Feb", 2: "Mar", 3: "Apr", 4: "May", 5: "Jun", 6: "Jul",
         7: "Aug", 8: "Sep", 9: "Oct", 10: "Nov", 11: "Dec"}
from FreeMono9pt7b import FreeMono9pt7b

xF = gfxFont( lcd, FreeMono9pt7b )
gfx = GFX(176, 220, lcd.drawPixel,
          hline=lcd.fastHline,
          vline=lcd.fastVline,
          fill_rect=lcd.fillRectangle,
          text=xF.text)
lcd.setOrientation(0)
gF = glcFont( lcd, TimesNR39x37, eraseMode=True )
lcd.setBackgroundColor( COLOR_BLUE )
cur_ampm = ""
cur_string = ""
sunrise = ""
sunset = ""

while True :
    (ut_offset, Tz) = get_TzInfo(lObject)
    now = get_localtime(ut_offset)
    h = now[3]
    m = now[4]
    s = now[5]
    d = now[2]
    mo = now[1]
    y= now[0]
    wkd = now[6]
    sun = Sun(now[2], now[1], now[0], 40.8438, -124.0645)

    
#    today = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(y, mo, d, h, m, s)
#    print(today)

    string = Day_str(wkd,mo-1,d)
    if string != cur_string:
        secs = sun.get_sunrise_time() + ut_offset
        hr, minute, second = parse_sec(secs)
        new_sunrise = "Sunrise {:02d}:{:02d}".format(hr,minute)
        print("Sunrise ", hr, minute)
        secs = sun.get_sunset_time() + ut_offset
        hr, minute, second = parse_sec(secs)
        print("Sunset ", hr, minute)
        new_sunset = "Sunset {:02d}:{:02d}".format(hr,minute)
        width = xF.getTextWidth(string)
        ww = int((lcd.maxX()-width)/2)
        xF.text(ww, 110, cur_string, COLOR_BLACK) #erase old
        xF.text(ww, 110, string, COLOR_ORANGE)
        xF.text(12, 85, sunrise, COLOR_BLACK) #erase old
        xF.text(12, 85, new_sunrise, COLOR_ORANGE)
        xF.text(18, 70, sunset, COLOR_BLACK) #erase old
        xF.text(18, 70, new_sunset, COLOR_ORANGE)
        sunrise = new_sunrise
        sunset = new_sunset
        cur_string = string
 
    if h >= 12 and h < 24 and m >= 0:
        ampm = "PM"
    else:
        ampm = "AM"
    if h > 12:
        h -= 12
    elif h == 0:
        h = 12
    time_str = "{0:02d}:{1:02d}".format(h,m)
    dx = 176 - gF.getTextWidth(time_str)
    xo = int(dx/2)
    if cur_ampm != ampm:
        gfx.fill_round_rect(xo-10,150,dx+30,43,5,COLOR_BLUE)
        xF.text(xo+85,150,ampm,COLOR_ORANGE)
        cur_ampm = ampm
    gF.text(xo, 150, time_str, COLOR_ORANGE)
    delay = 60 - s
    time.sleep(delay)
