import network
import urequests
import secrets
import time

from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
from pimoroni import RGBLED

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=270)

# set the display backlight to 20%
display.set_backlight(0.5)
display.set_font("sans")
display.set_thickness(2)

led = RGBLED(6, 7, 8)
led.set_rgb(0,0,0)

# set up constants for drawing
WIDTH, HEIGHT = display.get_bounds()
# setup some colours
RED = display.create_pen(209, 34, 41)
YELLOW = display.create_pen(255, 216, 0)
GREEN = display.create_pen(0, 216, 0)
WHITE = display.create_pen(255, 255, 255)
BLUE = display.create_pen(116, 215, 238)
BLACK = display.create_pen(0, 0, 0)

# Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
while not wlan.isconnected():
    pass
print('Connected to WLAN')



while True:
    # Make GivEnergy API call to get Inverter data
    url = "https://api.givenergy.cloud/v1/inverter/"+secrets.INVERTER+"/system-data/latest"
    headers = {
      'Authorization': 'Bearer '+ secrets.API_KEY,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }

    response = urequests.request('GET',url,headers=headers)
    data = response.json()
    batt_lvl = data['data']['battery']['percent']
    pwr_lvl = data['data']['battery']['power']
    print(batt_lvl)
    print(pwr_lvl)
    
    # fills the screen with black
    display.set_pen(WHITE)
    display.clear()
    
    # writes the battery level as text 
    display.set_pen(BLACK)
    display.text("BATTERY", 3, 20, 0, 1)
    
    if (batt_lvl <= 10):
        display.set_pen(RED)
        display.text("{:02d}".format(batt_lvl) + "%", 3, 60, 0, 2)
    elif (batt_lvl > 10):
        display.set_pen(GREEN)
        display.text("{:02d}".format(batt_lvl) + "%", 3, 60, 0, 2)
        
    display.set_pen(BLACK)
    display.text("POWER", 3, 100, 0, 1)
    display.text("{:04d}".format(pwr_lvl) + "W", 3, 140, 0, 1)

    
    # time to update the display
    display.update()
    
    #update the screen every 30 seconds with the API
    time.sleep(30)
 

