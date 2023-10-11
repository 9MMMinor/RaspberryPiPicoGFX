
from TimesNR16x16 import TimesNR16x16
from TimesNR39x37 import TimesNR39x37
from FreeMonoBoldOblique24pt7b import FreeMonoBoldOblique24pt7b
from F import F_Bitmap
from adafruit_gfx import GFX
from machine import Pin, SPI
from TFT_22_ILI9225 import TFT_22_ILI9225
from glcFont import glcFont
from gfxFont import gfxFont


# RGB 16-bit color table definition (RG565)
COLOR_BLACK          = 0x0000      #   0,   0,   0
COLOR_WHITE          = 0xFFFF      # 255, 255, 255
COLOR_BLUE           = 0x001F      #   0,   0, 255
COLOR_GREEN          = 0x07E0      #   0, 255,   0
COLOR_RED            = 0xF800      # 255,   0,   0
COLOR_NAVY           = 0x000F      #   0,   0, 128
COLOR_DARKBLUE       = 0x0011      #   0,   0, 139
COLOR_DARKGREEN      = 0x03E0      #   0, 128,   0
COLOR_DARKCYAN       = 0x03EF      #   0, 128, 128
COLOR_CYAN           = 0x07FF      #   0, 255, 255
COLOR_TURQUOISE      = 0x471A      #  64, 224, 208
COLOR_INDIGO         = 0x4810      #  75,   0, 130
COLOR_DARKRED        = 0x8000      # 128,   0,   0
COLOR_OLIVE          = 0x7BE0      # 128, 128,   0
COLOR_GRAY           = 0x8410      # 128, 128, 128
COLOR_GREY           = 0x8410      # 128, 128, 128
COLOR_SKYBLUE        = 0x867D      # 135, 206, 235
COLOR_BLUEVIOLET     = 0x895C      # 138,  43, 226
COLOR_LIGHTGREEN     = 0x9772      # 144, 238, 144
COLOR_DARKVIOLET     = 0x901A      # 148,   0, 211
COLOR_YELLOWGREEN    = 0x9E66      # 154, 205,  50
COLOR_BROWN          = 0xA145      # 165,  42,  42
COLOR_DARKGRAY       = 0x7BEF      # 128, 128, 128
COLOR_DARKGREY       = 0x7BEF      # 128, 128, 128
COLOR_SIENNA         = 0xA285      # 160,  82,  45
COLOR_LIGHTBLUE      = 0xAEDC      # 172, 216, 230
COLOR_GREENYELLOW    = 0xAFE5      # 173, 255,  47
COLOR_SILVER         = 0xC618      # 192, 192, 192
COLOR_LIGHTGRAY      = 0xC618      # 192, 192, 192
COLOR_LIGHTCYAN      = 0xE7FF      # 224, 255, 255
COLOR_VIOLET         = 0xEC1D      # 238, 130, 238
COLOR_AZUR           = 0xF7FF      # 240, 255, 255
COLOR_BEIGE          = 0xF7BB      # 245, 245, 220
COLOR_MAGENTA        = 0xF81F      # 255,   0, 255
COLOR_TOMATO         = 0xFB08      # 255,  99,  71
COLOR_GOLD           = 0xFEA0      # 255, 215,   0
COLOR_ORANGE         = 0xFD20      # 255, 165,   0
COLOR_SNOW           = 0xFFDF      # 255, 250, 250
COLOR_YELLOW         = 0xFFE0      # 255, 255,   0

_value = True
def isChange(value):
    global _value
    
    if value != _value:
        _value = value
        return True
    else:
        return False

spi = SPI(0, baudrate=40000000)
lcd = TFT_22_ILI9225(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))

import utime as time

day = {0: "Monday", 1: "Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday",
       6:"Sunday"}
rtc = machine.RTC()
# generate formated date/time strings from internal RTC
time_str = "{4:02d}:{5:02d}".format(*rtc.datetime())
print(time_str)

time_hour = time_str[:2]
time_minute = time_str.replace(time_hour,"",1)
time_minute = time_minute.replace(":","",1)
time_hour = int(time_hour)
time_minute = int(time_minute)
print(time_hour,time_minute)

from FreeMono9pt7b import FreeMono9pt7b

xF = gfxFont( lcd, FreeMono9pt7b )

gfx = GFX(176, 220, lcd.drawPixel,
          hline=lcd.fastHline,
          vline=lcd.fastVline,
          fill_rect=lcd.fillRectangle,
          text=xF.text)


lcd.setOrientation(0)
    
xF.text(10,90,"ABC",COLOR_BLUE)
xF.text(10,30,"abc",COLOR_YELLOW)
xF.text(10,60,"nop",COLOR_YELLOW)
xF.text(10,90,"ABC",COLOR_YELLOW)
xF.text(10,120,"NOP",COLOR_YELLOW)
time.sleep(2)
lcd.clear()

#xF = gfxFont( lcd, FreeMonoBoldOblique24pt7b )
gF = glcFont( lcd, TimesNR39x37, eraseMode=True )
lcd.setBackgroundColor( COLOR_BLUE )
drawBg = True
haschanged = False
(y,mo,d,wkd,h,m,s,tz) = rtc.datetime()
print(day[wkd])
while True :
    (y,mo,d,wkd,h,m,s,tz) = rtc.datetime()
    if h >= 12 and h < 24 and m >= 0:
        pm = True
        ampm = "PM"
    else:
        pm = False
        ampm = "AM"
    if h > 12:
        h -= 12
    elif h == 0:
        h = 12
    time_str = "{0:02d}:{1:02d}".format(h,m)
    dx = 176 - gF.getTextWidth(time_str)
    xo = int(dx/2)
    if isChange(pm):
        gfx.fill_round_rect(xo-10,150,dx+30,43,5,COLOR_BLUE)
        xF.text(xo+85,150,ampm,COLOR_ORANGE)
        drawBg = False
    gF.text(xo, 150, time_str, COLOR_ORANGE)
    time.sleep(1)
    
