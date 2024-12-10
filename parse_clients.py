import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = False
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

while True:
    clients = []
    with open('unformatted_output.txt') as file:
        line_num = 0
        next_ip = 2
        next_name = 3
        next_status = 9
        last_key = ""
        clients = []
        for line in file.readlines():
            line_num += 1

            if line_num == next_ip:
                last_key = line
                next_ip += 10

            if line_num == next_name:
                last_key = last_key + line
                next_name += 10

            if (line_num == next_status): 
                if line == 'on\n':
                    clients.append(last_key)
                next_status += 10

        #print(clients)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    Clients = "Clients: " + str(len(clients))
    # Write four lines of text.
    y = top
    draw.text((x, y), Clients, font=font, fill="#FFFFFF")
    y += font.getsize(Clients)[1]
    # draw.text((x, y), CPU, font=font, fill="#FFFF00")
    # y += font.getsize(CPU)[1]
    # draw.text((x, y), MemUsage, font=font, fill="#00FF00")
    # y += font.getsize(MemUsage)[1]
    # draw.text((x, y), Disk, font=font, fill="#0000FF")
    # y += font.getsize(Disk)[1]
    # draw.text((x, y), Temp, font=font, fill="#FF00FF")

    

    if buttonA.value and buttonB.value:
        backlight.value = False  # turn off backlight
    else:
        backlight.value = True  # turn on backlight
    # if buttonB.value and not buttonA.value:  # just button A pressed
    #     display.fill(color565(255, 0, 0))  # red
    # if buttonA.value and not buttonB.value:  # just button B pressed
    #     display.fill(color565(0, 0, 255))  # blue
    # if not buttonA.value and not buttonB.value:  # none pressed
    #     display.fill(color565(0, 255, 0))  # green
        
    # Display image.
    disp.image(image, rotation)
    time.sleep(0.1)

