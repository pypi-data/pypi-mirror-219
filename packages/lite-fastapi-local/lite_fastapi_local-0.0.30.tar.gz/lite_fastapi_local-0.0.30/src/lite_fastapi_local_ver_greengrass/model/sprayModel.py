import json

from common.variable import common
from settings import mqtt

class Spray():

    def turn_on_spray(self):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "spray":"on"
        }))

    def turn_off_spray(self):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "spray":"off"
        }))


    
spray = Spray()