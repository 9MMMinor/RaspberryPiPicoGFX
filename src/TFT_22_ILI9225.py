import time

# ILI9225 screen size
ILI9225_LCD_WIDTH = 176
ILI9225_LCD_HEIGHT = 220

R2L_BottomUp = 0
BottomUp_R2L = 1
L2R_BottomUp = 2
BottomUp_L2R = 3
R2L_TopDown  = 4
TopDown_R2L  = 5
L2R_TopDown  = 6
TopDown_L2R  = 7

modeTab = [
    [R2L_BottomUp, BottomUp_R2L, L2R_BottomUp, BottomUp_L2R, R2L_TopDown,  TopDown_R2L,  L2R_TopDown,  TopDown_L2R ],#0
    [BottomUp_L2R, L2R_BottomUp, TopDown_L2R,  L2R_TopDown,  BottomUp_R2L, R2L_BottomUp, TopDown_R2L,  R2L_TopDown ],#90   
    [L2R_TopDown , TopDown_L2R,  R2L_TopDown,  TopDown_R2L,  L2R_BottomUp, BottomUp_L2R, R2L_BottomUp, BottomUp_R2L],#180
    [TopDown_R2L , R2L_TopDown,  BottomUp_R2L, R2L_BottomUp, TopDown_L2R,  L2R_TopDown,  BottomUp_L2R, L2R_BottomUp] #270
          ]
    

# ILI9225 LCD Registers
ILI9225_DRIVER_OUTPUT_CTRL      = (0x01)  # Driver Output Control
ILI9225_LCD_AC_DRIVING_CTRL     = (0x02)  # LCD AC Driving Control
ILI9225_ENTRY_MODE              = (0x03)  # Entry Mode
ILI9225_DISP_CTRL1              = (0x07)  # Display Control 1
ILI9225_BLANK_PERIOD_CTRL1      = (0x08)  # Blank Period Control
ILI9225_FRAME_CYCLE_CTRL        = (0x0B)  # Frame Cycle Control
ILI9225_INTERFACE_CTRL          = (0x0C)  # Interface Control
ILI9225_OSC_CTRL                = (0x0F)  # Osc Control
ILI9225_POWER_CTRL1             = (0x10)  # Power Control 1
ILI9225_POWER_CTRL2             = (0x11)  # Power Control 2
ILI9225_POWER_CTRL3             = (0x12)  # Power Control 3
ILI9225_POWER_CTRL4             = (0x13)  # Power Control 4
ILI9225_POWER_CTRL5             = (0x14)  # Power Control 5
ILI9225_VCI_RECYCLING           = (0x15)  # VCI Recycling
ILI9225_RAM_ADDR_SET1           = (0x20)  # Horizontal GRAM Address Set
ILI9225_RAM_ADDR_SET2           = (0x21)  # Vertical GRAM Address Set
ILI9225_GRAM_DATA_REG           = (0x22)  # GRAM Data Register
ILI9225_GATE_SCAN_CTRL          = (0x30)  # Gate Scan Control Register
ILI9225_VERTICAL_SCROLL_CTRL1   = (0x31)  # Vertical Scroll Control 1 Register
ILI9225_VERTICAL_SCROLL_CTRL2   = (0x32)  # Vertical Scroll Control 2 Register
ILI9225_VERTICAL_SCROLL_CTRL3   = (0x33)  # Vertical Scroll Control 3 Register
ILI9225_PARTIAL_DRIVING_POS1    = (0x34)  # Partial Driving Position 1 Register
ILI9225_PARTIAL_DRIVING_POS2    = (0x35)  # Partial Driving Position 2 Register
ILI9225_HORIZONTAL_WINDOW_ADDR1 = (0x36)  # Horizontal Address Start Position
ILI9225_HORIZONTAL_WINDOW_ADDR2 = (0x37)  # Horizontal Address End Position
ILI9225_VERTICAL_WINDOW_ADDR1   = (0x38)  # Vertical Address Start Position
ILI9225_VERTICAL_WINDOW_ADDR2   = (0x39)  # Vertical Address End Position
ILI9225_GAMMA_CTRL1             = (0x50)  # Gamma Control 1
ILI9225_GAMMA_CTRL2             = (0x51)  # Gamma Control 2
ILI9225_GAMMA_CTRL3             = (0x52)  # Gamma Control 3
ILI9225_GAMMA_CTRL4             = (0x53)  # Gamma Control 4
ILI9225_GAMMA_CTRL5             = (0x54)  # Gamma Control 5
ILI9225_GAMMA_CTRL6             = (0x55)  # Gamma Control 6
ILI9225_GAMMA_CTRL7             = (0x56)  # Gamma Control 7
ILI9225_GAMMA_CTRL8             = (0x57)  # Gamma Control 8
ILI9225_GAMMA_CTRL9             = (0x58)  # Gamma Control 9
ILI9225_GAMMA_CTRL10            = (0x59)  # Gamma Control 10

ILI9225C_INVOFF  = 0x20
ILI9225C_INVON   = 0x21

ILI9225_START_BYTE = 0x005C


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


def color565(r, g, b):
    """Return RGB565 color value.
    Args:
        r (int): Red value.
        g (int): Green value.
        b (int): Blue value.
    """
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3


def clamp(v, min_v, max_v):
    return min(max(v, min_v), max_v)


class TFT_22_ILI9225():
    ''' Display package

    public:
        display_object = TFT_22_ILI9225(spi, cs, dc, rst, width=176, height=220, rotation=0, led=255)
    '''
        
    ### Initialization
    ROTATE = {
        0: 0x88,
        90: 0xE8,
        180: 0x48,
        270: 0x28
    }

    # Constructor when using hardware SPI.  Faster, but must use SPI pins
    # specific to each board type (e.g. 11,13 for Uno, 51,52 for Mega, etc.)
    # Adds backlight brightness 0-255
    def __init__(self, spi, cs, dc, rst,
        width=ILI9225_LCD_WIDTH, height=ILI9225_LCD_HEIGHT, rotation=0, led=255):

        _spi  = spi
        self.spi = spi
        _cs   = cs
        _dc   = dc
        _rst  = rst
        self.width = width
        self._maxX = width
        self.height = height
        self._maxY = height
        self._orientation = rotation
        self._bgColor = COLOR_BLACK
        hwSPI = True
        blState = False
        writeFunctionLevel = 0
        gfxFont = None
        self.font = None
        if rotation not in self.ROTATE.keys():
            raise RuntimeError('Rotation must be 0, 90, 180 or 270.')
        else:
            self.rotation = self.ROTATE[rotation]
    ## Set up reset pin
        self.rst = rst
        self.rst.init(self.rst.OUT, value=0)
    ## Control pins
        self.dc = dc
        self.dc.init(self.dc.OUT, value=0)
        self.cs = cs
        self.cs.init(self.dc.OUT, value=1)

    ## Initialization Code
        self.reset()                # reset ILI9225
        self.setup()

    ## Turn on backlight
#        self.setBacklight(True)
        self.setOrientation(0)

    ## Initialize variables
        self.clear()
        
    ## Start Initial sequence        
    def setup(self):
        self.writeRegister(ILI9225_DRIVER_OUTPUT_CTRL, 0x031C)   # set the display line number and display direction
        self.writeRegister(ILI9225_LCD_AC_DRIVING_CTRL, 0x0100)  # set 1 line inversion
        self.writeRegister(ILI9225_ENTRY_MODE, 0x1030)           # set GRAM write direction and BGR=1.
        self.writeRegister(ILI9225_BLANK_PERIOD_CTRL1, 0x0808)   # set the back porch and front porch
        self.writeRegister(ILI9225_INTERFACE_CTRL, 0x0000)       # CPU interface
        self.writeRegister(ILI9225_OSC_CTRL, 0x0801)             # set Osc  /*0e01*/
        self.writeRegister(ILI9225_RAM_ADDR_SET1, 0x0000)        # RAM Address
        self.writeRegister(ILI9225_RAM_ADDR_SET2, 0x0000)        # RAM Address

        # Power On sequence
        time.sleep_ms(50)
        self.writeRegister(ILI9225_POWER_CTRL1, 0x0A00)  # set SAP,DSTB,STB
        self.writeRegister(ILI9225_POWER_CTRL2, 0x1038)  # set APON,PON,AON,VCI1EN,VC
        time.sleep_ms(50)
        self.writeRegister(ILI9225_POWER_CTRL3, 0x1121)  # set BT,DC1,DC2,DC3
        self.writeRegister(ILI9225_POWER_CTRL4, 0x0066)  # set GVDD
        self.writeRegister(ILI9225_POWER_CTRL5, 0x5F60)  # set VCOMH/VCOML voltage

        # Set GRAM area
        self.writeRegister(ILI9225_GATE_SCAN_CTRL, 0x0000)
        self.writeRegister(ILI9225_VERTICAL_SCROLL_CTRL1, 0x00DB)
        self.writeRegister(ILI9225_VERTICAL_SCROLL_CTRL2, 0x0000)
        self.writeRegister(ILI9225_VERTICAL_SCROLL_CTRL3, 0x0000)
        self.writeRegister(ILI9225_PARTIAL_DRIVING_POS1, 0x00DB)
        self.writeRegister(ILI9225_PARTIAL_DRIVING_POS2, 0x0000)
        self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR1, 0x00AF)
        self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR2, 0x0000)
        self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR1, 0x00DB)
        self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR2, 0x0000)

        # Adjust GAMMA curve
        self.writeRegister(ILI9225_GAMMA_CTRL1, 0x4000)
        self.writeRegister(ILI9225_GAMMA_CTRL2, 0x060B)
        self.writeRegister(ILI9225_GAMMA_CTRL3, 0x0C0A)
        self.writeRegister(ILI9225_GAMMA_CTRL4, 0x0105)
        self.writeRegister(ILI9225_GAMMA_CTRL5, 0x0A0C)
        self.writeRegister(ILI9225_GAMMA_CTRL6, 0x0B06)
        self.writeRegister(ILI9225_GAMMA_CTRL7, 0x0004)
        self.writeRegister(ILI9225_GAMMA_CTRL8, 0x0501)
        self.writeRegister(ILI9225_GAMMA_CTRL9, 0x0E00)
        self.writeRegister(ILI9225_GAMMA_CTRL10, 0x000E)

        time.sleep_ms(50)

        self.writeRegister(ILI9225_DISP_CTRL1, 0x1017)


    def reset(self):
        self.rst.on()         ## Pull the reset pin high to release the ILI9225C from the reset status
        time.sleep_ms(1)
        self.rst.off()        ## Pull the reset pin low to reset ILI9225
        time.sleep_ms(10)
        self.rst.on()         ## Pull the reset pin high to release the ILI9225C from the reset status
        time.sleep_ms(50)


    def _orientCoordinates(self, x1, y1):
        case = self._orientation
        if case == 0:
            return (x1,y1)
        elif case == 1:
            y1 = self._maxY - y1 - 1
            (x1, y1) = (y1,x1)    # swap
            return (x1,y1)
        elif case == 2:
            x1 = self._maxX - x1 - 1
            y1 = self._maxY - y1 - 1
            return (x1,y1)
        elif case == 3:
            x1 = self._maxX - x1 - 1
            (x1, y1) = (y1,x1)    # swap
            return (x1,y1)


    def _setWindow(self, x0, y0, x1, y1):
        self._setWindowMode( x0, y0, x1, y1, BottomUp_L2R )  ## default for drawing characters
 
 
    def _setGFXWindow(self, x0, y0, x1, y1):
        self._setWindowMode( x0, y0, x1, y1, 0)  ## default for drawing characters


    def _setWindowMode(self, x0, y0,  x1, y1, mode):    # mode=autoIncMode
        ## clip to TFT-Dimensions
        x0 = clamp( x0, 0, (self._maxX-1) )
        x1 = clamp( x1, 0, (self._maxX-1) )
        y0 = clamp( y0, 0, (self._maxY-1) )
        y1 = clamp( y1, 0, (self._maxY-1) )
        (x0,y0) = self._orientCoordinates(x0, y0)
        (x1,y1) = self._orientCoordinates(x1, y1)

        if (x1<x0):
            (x0, x1) = x1,x0
        if (y1<y0):
            (y0, y1) = y1,y0
    
        dmode = modeTab[self._orientation][mode]

        self.writeRegister(ILI9225_ENTRY_MODE, 0x1000 | ( dmode<<3) )    #BGR | I/D | AM
        self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR1,x1)
        self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR2,x0)

        self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR1,y1)
        self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR2,y0)

        case = dmode>>1
        if case==0:
            self.writeRegister(ILI9225_RAM_ADDR_SET1,x1)
            self.writeRegister(ILI9225_RAM_ADDR_SET2,y1)
        elif case==1:
            self.writeRegister(ILI9225_RAM_ADDR_SET1,x0)
            self.writeRegister(ILI9225_RAM_ADDR_SET2,y1)
        elif case==2:
            self.writeRegister(ILI9225_RAM_ADDR_SET1,x1)
            self.writeRegister(ILI9225_RAM_ADDR_SET2,y0)
        elif case==3:
            self.writeRegister(ILI9225_RAM_ADDR_SET1,x0)
            self.writeRegister(ILI9225_RAM_ADDR_SET2,y0)
        self._writeCommand( ILI9225_GRAM_DATA_REG )


    def _resetWindow(self):
        self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR1, 0x00AF)     #0x00AF
        self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR2, 0x0000)
        self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR1, 0x00DB)       #0x00DB
        self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR2, 0x0000)


    def clear(self):
        old = self._orientation
        self.setOrientation(0)
        self.fillRectangle(0, 0, self._maxX, self._maxY, self._bgColor)
        self.setOrientation(old)
        time.sleep_ms(10 )


    def writeRegister(self, reg, data):
        self.cs(0)
        self.dc(0)
        self.spi.write(reg.to_bytes(2,'big'))
        self.dc(1)
        self.spi.write(data.to_bytes(2,'big'))
        self.cs(1)


    def _writeData(self, data):
        self.cs(0)
        self.dc(1)
        self.spi.write(data.to_bytes(2,'big'))
        self.cs(1)


    def _writeCommand(self, reg):
        self.cs(0)
        self.dc(0)
        self.spi.write(reg.to_bytes(2,'big'))
        self.cs(1)


###     Switch display on or off
###     @param     flag true=on, false=off
    def setDisplay(self, flag):
        if (flag):
            self.writeRegister(0x00ff, 0x0000)
            self.writeRegister(ILI9225_POWER_CTRL1, 0x0000)
            time.sleep_ms(50)
            self.writeRegister(ILI9225_DISP_CTRL1, 0x1017)
            time.sleep_ms(200)
        else:
            self.writeRegister(0x00ff, 0x0000)
            self.writeRegister(ILI9225_DISP_CTRL1, 0x0000)
            time.sleep_ms(50)
            self.writeRegister(ILI9225_POWER_CTRL1, 0x0003)
            time.sleep_ms(200)

###     Set orientation
###     0=portrait, 1=right rotated landscape, 2=reverse portrait, 3=left rotated landscape
    def setOrientation(self, orientation):
        self._orientation = orientation % 4
        case = self._orientation
        if case == 0:
            self._maxX = ILI9225_LCD_WIDTH
            self._maxY = ILI9225_LCD_HEIGHT
        elif case == 1:
            self._maxX = ILI9225_LCD_HEIGHT
            self._maxY = ILI9225_LCD_WIDTH
        elif case == 2:
            self._maxX = ILI9225_LCD_WIDTH
            self._maxY = ILI9225_LCD_HEIGHT
        elif case == 3:
            self._maxX = ILI9225_LCD_HEIGHT
            self._maxY = ILI9225_LCD_WIDTH


    def getOrientation(self):
        return self._orientation


    def setBackgroundColor(self, color):
        self._bgColor = color


    def getBackgroundColor(self):
        return self._bgColor
    
    
    def drawPixel(self, x1, y1, color):
        if((x1 >= self._maxX) or (y1 >= self._maxY)):
            return
        (x1,y1) = self._orientCoordinates(x1, y1)
        self.writeRegister(ILI9225_RAM_ADDR_SET1,x1)
        self.writeRegister(ILI9225_RAM_ADDR_SET2,y1)
        self.writeRegister(ILI9225_GRAM_DATA_REG,color)

    def fillRectangle(self, x1, y1, width, height, color):
        x2 = x1+width-1
        y2 = y1+height-1
        self._setWindow(x1, y1, x2, y2)
        t=(y2 - y1 + 1) * (x2 - x1 + 1)
        self.cs(0)
        self.dc(1)
        while t > 0:
            self.spi.write(color.to_bytes(2,'big'))
            t -= 1
        self.cs(1)
        self._resetWindow()


    def fastHline(self, x, y, width, color):
        self.fillRectangle(x, y, width, 1, color)


    def fastVline(self, x, y, height, color):
        self.fillRectangle(x, y, 1, height, color)