import json

from lite_fastapi_local.common.variable import common
from lite_fastapi_local.settings import mqtt

class Sol():

    def turn_on_sol(self, index):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "do":{
                "index": str(index),
                "control": "1"
            }
        }))

    def turn_off_sol(self, index):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "do":{
                "index": str(index),
                "control": "0"
            }
        }))


    
sol = Sol()