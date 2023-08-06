import json

from lite_fastapi_local.common.variable import common
from lite_fastapi_local.settings import mqtt

class BoxDoor():

    def open_box_door(self):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "door":"open"
        }))

    def close_box_door(self):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "door":"close"
        }))


    
box_door = BoxDoor()