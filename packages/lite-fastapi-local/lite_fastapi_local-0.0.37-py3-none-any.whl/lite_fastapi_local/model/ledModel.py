import json

from lite_fastapi_local.common.variable import common
from lite_fastapi_local.settings import mqtt

class Led():

    def turn_on_led(self):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "led":"on"
        }))

    def turn_off_led(self):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "led":"off"
        }))


    
led = Led()