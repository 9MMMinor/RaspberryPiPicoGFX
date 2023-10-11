import struct

class gfxFont(object):
    """Font structures for newer Adafruit_GFX (1.1 and later).

    Font structures for newer Adafruit_GFX (1.1 and later).
    Example fonts are included in 'Fonts' directory.
    To use a font in your Micropython script, import the corresponding .py
    file and pass Font tuple to the class __init__, e.g.
    
    from FreeMono9pt7b import FreeMono9pt7b
    
    bitmap = array.array('B', [...])

    Font data stored PER GLYPH
    glyph = (
            bitmapOffset,   # Offset into GFXfont bitmap
            width,          # Bitmap dimensions in pixels
            height,         # Bitmap dimensions in pixels
            xAdvance,       # Distance to advance cursor (x axis)
            xOffset,        # X dist from cursor pos to UL corner
            yOffset)        # Y dist from cursor pos to UL corner

    Data tuple for FONT AS A WHOLE
    Font = (
            bitmap          # Bitmaps array of bytes
            glyph           # Glyph array of integers
            first           # ASCII extents (first char)
            last            # ASCII extents (last char)
            yAdvance)       # Newline distance (y axis)

    """


    def __init__(self, tft, fontTuple):
        '''
        Attributes:
            tft: TFT_22_ILI9225 display object.
            fontTuple: Data tuple for FONT AS A WHOLE
        '''
        (self._gfxBitmap, self._gfxGlyph, self._gfxOrdFirstCh, self._gfxOrdLastCh, self._gfxGlylen) = fontTuple
        self._gfxGlylen = struct.calcsize('iiiiii')
        self.display = tft


    def setGFXFont(self, f):
        (self._gfxBitmap, self._gfxGlyph, self._gfxOrdFirstCh, self._gfxOrdLastCh, self._yAdvance) = f #font Tuple


## Draw a string
    def text(self, x, y, s, color):
        currx = x
        k = 0
        while k < len(s):
            currx += self.drawChar(currx, y, s[k], color) + 1
            k+=1
        return currx

## Draw a character
    def drawChar(self, x, y, ch, color):
        Barray = self._gfxBitmap
        Garray = self._gfxGlyph
        Goff = int((ord(ch) - self._gfxOrdFirstCh) * self._gfxGlylen)
        (bo,w,h,xa,xo,yo) = struct.unpack_from('iiiiii', Garray, Goff)
        
        bits = 0
        bit = 0
        _orient = self.display.getOrientation()
        self.display.setOrientation(_orient+2)
        y = self.display._maxY - y - 1      
        yy=0
        while yy<h: #for yy in range(h):
            xx=0
            while xx<w:
                if(not(bit & 7)):
                    bits = Barray[bo]
                    bo+=1
                bit+=1
                if(bits & 0x80):
                    x1 = x+xx+xo
                    x1=self.display._maxX - x1
                    self.display.drawPixel(x1, y+yy+yo, color)
                bits <<= 1
                xx+=1
            yy+=1
        self.display.setOrientation(_orient)
#        return xa
        return w


    def getCharExtent(self, ch):
        Garray = self._gfxGlyph
        if (ord(ch) < self._gfxOrdFirstCh) or (ord(ch) > self._gfxOrdLastCh):
            return (0, 0, 0)
        Goff = int((ord(ch) - self._gfxOrdFirstCh) * self._gfxGlylen)
        (bo,w,h,xa,xo,yo) = struct.unpack_from('iiiiii', Garray, Goff)
        return (w, h, xa)


    def getCharWidth(self, ch):
        (w,h,xa) = self.getCharExtent(ch)
        return w


    def getTextExtent(self, str):
        k = 0
        w = 0
        h = 0
        while  k < len(str):
            (gw, gh, xa) = self.getCharExtent(str[k])
            if (gh > h):
                h = gh
            w += xa
            k += 1
        return (w, h, xa)


    def getTextWidth(self, str):
        (w,h,xa) = self.getTextExtent(str)
        return w