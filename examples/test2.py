import utime as time
from machine import Pin, SPI
from adafruit_gfx import GFX
from TimesNR16x16 import TimesNR16x16
from FreeMono9pt7b import FreeMono9pt7b
from TFT_22_ILI9225 import TFT_22_ILI9225
from glcFont import glcFont
from gfxFont import gfxFont
#from gfx_standard_font_01 import text_dict as std_font
import struct
from tux import TuxBitmap


COLOR_BLACK          = 0x0000      #   0,   0,   0
COLOR_WHITE          = 0xFFFF      # 255, 255, 255
COLOR_GREEN          = 0x07E0      #   0, 255,   0
COLOR_RED            = 0xF800      # 255,   0,   0
COLOR_YELLOW         = 0xFFE0      # 255, 255,   0

orientation = {0:"Portrait", 1:"right rotated Landscape", 2:"reverse Portrait", 3:"left rotated Landscape"}
    

spi = SPI(0)
d=TFT_22_ILI9225(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))
d.clear()
f=glcFont(d,TimesNR16x16)
#f=glcFont(d,TimesNR16x16, eraseMode=True)
fx = gfxFont(d, FreeMono9pt7b)
gfx = GFX(176, 220, d.drawPixel,
          hline=d.fastHline,
          vline=d.fastVline,
          fill_rect=d.fillRectangle)
          #text=f.text)
          #font=std_font)

f=glcFont(d,TimesNR16x16)
fx = gfxFont(d, FreeMono9pt7b)
origin = "gfx Origin"
ww = fx.getTextWidth(origin)
print("gfxFont TextWidth:",ww)
d.setBackgroundColor(COLOR_YELLOW)
for i in range(4):
    d.clear()
    d.setOrientation(i)
    f.text(0,50,"abcdef",COLOR_GREEN)
    if i == 3:
        gfx.set_text_background()
    else:
        gfx.set_text_background(COLOR_GREEN)
    gfx.text(0,20,"ABCDEF",4,COLOR_RED)
    f.text(0,70,"ABCDEF",COLOR_GREEN)
    f.text(0,90,orientation[i],COLOR_GREEN)
    ww=fx.text(0, 5, origin, COLOR_RED)
    gfx.line(0,5,ww,5,COLOR_RED)
    time.sleep(5)
time.sleep(10)
d.setOrientation(0)
d.clear()
gfx.fill_rect(20,20,100,100,COLOR_GREEN)
gfx.fill_circle(120,120,20,COLOR_GREEN)
gfx.rect(20,20,100,100,COLOR_RED)
time.sleep(2)
d.clear()
gfx.drawBitmap(20, 40, TuxBitmap, COLOR_WHITE)


