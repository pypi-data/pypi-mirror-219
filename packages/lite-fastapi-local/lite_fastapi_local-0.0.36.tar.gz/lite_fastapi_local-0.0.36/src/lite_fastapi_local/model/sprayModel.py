import json

from lite_fastapi_local.common.variable import common
from lite_fastapi_local.settings import mqtt

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