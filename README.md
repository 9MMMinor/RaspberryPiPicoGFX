# RaspberryPiPicoGFX
Micropython graphics (GFX) and fonts for ILI9225 display for Raspberry Pi Pico

TFT_22_ILI9225.py
adafruit_gfx.py
gfxFont.py
glcFont.py

Python code 
==============
The following code has been tested on Raspberry Pi Pico W. With the exception of the examples,
all .py modules were saved to the Raspberry Pi Pico using, for example, Thonny.

The driver object, TFT_22_ILI9225, is derived from:
[v1.4.5](https://github.com/Nkawu/TFT_22_ILI9225/releases/tag/v1.4.5)

The graphics library object, GFX, is minimally edited from CircuitPython pixel graphics drawing library:
(https://github.com/adafruit/Adafruit_CircuitPython_GFX.git).
A Method, drawBitmap, to draw XBitMap files (.xbm) exported from GIMP, has been added.

A font object, glcFont, is derived from font methods found in:
(https://github.com/Nkawu/TFT_22_ILI9225/releases/tag/v1.4.5),
which use fonts generated by MikroElektronika GLCD Font Creator 1.2.0.0,
MikroElektronika 2011, http://www.mikroe.com.

A font object, gfxFont, is derived from font method, drawGFXChar(), found in
TFT_22_ILI9225.cpp (see github.com/Nkawu, above), in which character glyphs are separated from the
character bitmaps. These are the font structures used in Adafruit_GFX 1.1 and later.



## Introduction

This is a library for the ILI9225 based 2.2" 176x220 TFT LCD shields commonly found on eBay,
originally forked from the screen_4D_22_library library. The ability to use GLCD fonts has been added
and the syntax has been changed to match the Adafruit libraries somewhat.


## Documentation

Documentation describing physical module connections can be found in the repo's
 **[Wiki](https://github.com/Nkawu/TFT_22_ILI9225/wiki)**


## Classes and methods

    class TFT_22_ILI9225()
        spi_object = SPI(0))
        lcd_object = TFT_22_ILI9225(spi_object, dc=Pin(15), cs=Pin(17), rst=Pin(14))

    Methods
        reset()
            perform a reset to the ILI9225 chip
        clear()
            fill the entire screen with black pixels
        setDisplay(flag)
            switch the display on (flag=True) or off (flag=False)
        setOrientation(orientation)
            set the coordinate orientation of the screen:
            0=portrait, 1=right rotated landscape, 2=reverse portrait, 3=left rotated landscape
        getOrientation()
            returns the current orientation
        setBackgroundColor(color)
            set background color to "color"
        getBackgroundColor()
            return background color
        maxX()
            returns maximum screen X dimension
        maxY()
            returns maximum screen Y dimension
            
    The folowing methods are typically screen driver primatives passed to the GFX class:
         
        drawPixel(x, y, color)
            draw the pixel at (x,y) with "color"
        fillRectangle(x, y, width, height, color)
            fill rectangle of width and height lower left corner at (x,y) with "color"
        fastHline(x, y, width, color)
            draws horizontal "color"ed line of width            
        fastVline(x, y, height, color)
            draws vertical "color"ed line of height


    class GFX()
        gfx_object = GFX(width, height, pixel,
            hline=Hline,        # A function to quickly draw a horizontal line on the display
            vline=Vline,        # A function to quickly draw a vertical line on the display
            fill_rect=fillRect, # A function to quickly draw a solid rectangle
            text=drawText,      # A function to quickly place text on the screen
            font=Font           # Alternative dict font
            )
        where "width" is the drawing area width in pixels,
        "height" is the drawing area height in pixels,
        and "pixel" is a function to call when a pixel is drawn on the display (see driver methods above).

    Methods
        pixel(x, y, color)
            draw a pixel at x,y
        rect(x, y, width, heigth, color)
            draw a single pixel wide rectangle of width x height with (x,y) at the bottom left
        fill_rect(x, y, width, height, color)
            draw a filled rectangle of width x height with (x,y) at the bottom left
        hline(x, y, width, color)
            draw a horzontal line of width starting from (x,y)
        vline(x, y, height, color)
            draw a vertical line of height starting from (x,y)
        line(x0, y0, x1, y1, color)
            draw a single pixel wide line starting at x0, y0 and ending at x1, y1
        circle(x0, y0, radius, color)
            draw a single pixel wide circle with center at x0, y0 and the specified radius
        fill_circle(x0, y0, radius, color)
            draw a filled circle with center at x0, y0 and the specified radius
        triangle(x0, y0, x1, y1, x2, y2, color)
            draw a single pixel wide triangle around the points (x0, y0), (x1, y1), and (x2, y2)
        fill_triangle(x0, y0, x1, y1, x2, y2, color)
            draw a filled triangle around the points (x0, y0), (x1, y1), and (x2, y2)
        round_rect(x0, y0, width, height, radius, color)
            draw the outline of a rectangle with rounded corners of radius with (x0,y0) at the bottom left
        fill_round_rect(x0, y0, width, height, radius, color)
            draw a filled rectangle with rounded corners of radius with (x0,y0) at the bottom left
        text(x, y, string, size, color)
            draw string starting at (x,y) of size using internal dictionary font.
        drawBitmap(x, y, bitmapTuple, color, bg=0, transparent=True, Xbit=True)
            draw XBitMap Files (.xbm) exported from GIMP with (x,y) at the bottom left, where bitmapTuple
            is (bitmap_array, width, height).
            
            
    class glcFont()
        A class to represent a GLCD font in X-GLCD format

        Font Generated by MikroElektronika GLCD Font Creator 1.2.0.0
        MikroElektronika 2011 
        http://www.mikroe.com
    
        glcFont_object = glcFont(tft, font,
            monoSp=False,   # default use individual char widths. monoSp=True, use fixed width chars.
            eraseMode=False # default char written without background. eraseMode=True, write background.
            )
            tft: TFT_22_ILI9225 display object.
            font: A bytearray of characters (each row of self.offset bytes represents a character).
                font[0] = width: Maximum pixel width of font.
                font[1] = height: Pixel height of font.
                font[2] = start_char: ASCII ordinate of first character.
                font[3] = number of characters in the bytearray.
                font[offset] = width of individual character in pixels.
    Methods:
        text(x, y, string, color)
            prints text string beginning at (x,y). Returns x-coordinate for next character print.
        getFontParams()
            returns tuple, [offset, width, height, bytes_per_character] for overall font.
        getTextWidth(string)
            returns string width in pixels.


class gfxFont():
    A class to represent structures for newer Adafruit_GFX (1.1 and later).
    
    Example fonts are included in 'Fonts' directory.
    To use a font in your Micropython script, import the corresponding .py
    file and pass Font tuple to the class __init__, e.g.
        from FreeMono9pt7b import FreeMono9pt7b
        fx = gfxFont(display_object, FreeMono9pt7b)
    
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

    Methods:
        text(x, y, string, color)
            prints text string beginning at (x,y). Returns x-coordinate for next character print.
        getTextWidth(string)
            returns string width in pixels.
