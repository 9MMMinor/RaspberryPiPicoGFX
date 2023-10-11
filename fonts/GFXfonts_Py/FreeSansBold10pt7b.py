# Adafruit GFX font
## Font structures for newer Adafruit_GFX (1.1 and later).
## Example fonts are included in 'Fonts' directory.
## To use a font in your Micropython script, import the corresponding .py
## file and pass the name of GFXfont to setFont().

## Font data stored PER GLYPH
#Glyph = (
#  bitmapOffset,    ## Offset into GFXfont bitmap
#  width,           ## Bitmap dimensions in pixels
#  height,          ## Bitmap dimensions in pixels
#  xAdvance,        ## Distance to advance cursor (x axis)
#  xOffset,         ## X dist from cursor pos to UL corner
#  yOffset)         ## Y dist from cursor pos to UL corner
#

## Data stored for FONT AS A WHOLE
#Font = (
#  bitmap           ## Bitmaps array of bytes
#  glyph            ## Glyph array of integers
#  first            ## ASCII extents (first char)
#  last             ## ASCII extents (last char)
#  yAdvance)        ## Newline distance (y axis)
#

import array, struct

FreeSansBold10pt7bBitmaps = array.array('B', [
  0x18, 0x31, 0x7B, 0xF3, 0x85, 0x89, 0x00, 0x0C, 0x03, 0x00, 0xC3, 0xFF,
  0xFF, 0xFF, 0xF0, 0xC0, 0x30, 0x0C, 0x00, 0xFF, 0x93, 0x80, 0xFF, 0xFE,
  0xFF, 0x80, 0x08, 0x21, 0x84, 0x10, 0x43, 0x08, 0x21, 0x84, 0x10, 0x43,
  0x00, 0x3E, 0x3F, 0xB8, 0xFC, 0x7E, 0x3E, 0x0F, 0x07, 0x83, 0xC1, 0xF1,
  0xF8, 0xFC, 0x77, 0xF1, 0xF0, 0x0E, 0x1F, 0xFF, 0xF0, 0xE1, 0xC3, 0x87,
  0x0E, 0x1C, 0x38, 0x70, 0xE1, 0xC0, 0x7F, 0x7F, 0xF8, 0xFC, 0x7C, 0x38,
  0x1C, 0x1E, 0x1E, 0x1E, 0x1C, 0x1C, 0x1F, 0xFF, 0xFF, 0xFC, 0x7F, 0x7F,
  0xB8, 0xF8, 0x70, 0x38, 0x38, 0x78, 0x3F, 0x03, 0x81, 0xF0, 0xFC, 0x7F,
  0xFB, 0xF8, 0x07, 0x81, 0xE0, 0xF8, 0x7E, 0x1B, 0x8C, 0xE3, 0x39, 0x8E,
  0xC3, 0xBF, 0xFF, 0xFC, 0x0E, 0x03, 0x80, 0xE0, 0x7F, 0xBF, 0xD8, 0x0C,
  0x0E, 0xC7, 0xFB, 0xFF, 0xC7, 0x03, 0x80, 0xF0, 0xFC, 0x7F, 0xF3, 0xF0,
  0x3F, 0x3F, 0xF8, 0xFC, 0x0E, 0x06, 0xFB, 0xFF, 0xC7, 0xE1, 0xE0, 0xF8,
  0x7C, 0x77, 0xF1, 0xF8, 0xFF, 0xFF, 0xF0, 0x38, 0x0C, 0x07, 0x03, 0x80,
  0xE0, 0x70, 0x1C, 0x06, 0x03, 0x80, 0xE0, 0x38, 0x0E, 0x00, 0x3F, 0x8F,
  0xF9, 0xC7, 0x30, 0x67, 0x1C, 0x7F, 0x0F, 0xE3, 0xDE, 0x71, 0xDC, 0x1B,
  0x83, 0x38, 0xE7, 0xFC, 0x7F, 0x00, 0x7E, 0x7F, 0xB8, 0xF8, 0x7C, 0x3E,
  0x1F, 0x8F, 0xFF, 0x7D, 0x81, 0xC0, 0xFC, 0x7F, 0xF3, 0xF0 ])

FreeSansBold10pt7bGlyphs = array.array('i', [
       0,   7,   7,   8,    0,  -14,   # 0x2A '*'
       7,  10,   9,  12,    1,   -8,   # 0x2B '+'
      19,   3,   6,   6,    1,   -2,   # 0x2C ','
      22,   5,   3,   7,    1,   -6,   # 0x2D '-'
      24,   3,   3,   6,    1,   -2,   # 0x2E '.'
      26,   6,  14,   6,    0,  -13,   # 0x2F '/'
      37,   9,  14,  11,    1,  -13,   # 0x30 '0'
      53,   7,  14,  11,    1,  -13,   # 0x31 '1'
      66,   9,  14,  11,    1,  -13,   # 0x32 '2'
      82,   9,  14,  11,    1,  -13,   # 0x33 '3'
      98,  10,  14,  11,    0,  -13,   # 0x34 '4'
     116,   9,  14,  11,    1,  -13,   # 0x35 '5'
     132,   9,  14,  11,    1,  -13,   # 0x36 '6'
     148,  10,  14,  11,    1,  -13,   # 0x37 '7'
     166,  11,  14,  11,    0,  -13,   # 0x38 '8'
     186,   9,  14,  11,    1,  -13 ]) # 0x39 '9'

FreeSansBold10pt7b   = (
  FreeSansBold10pt7bBitmaps,
  FreeSansBold10pt7bGlyphs,
  0x2A, 0x39, 35 ) # Approx. 321 bytes