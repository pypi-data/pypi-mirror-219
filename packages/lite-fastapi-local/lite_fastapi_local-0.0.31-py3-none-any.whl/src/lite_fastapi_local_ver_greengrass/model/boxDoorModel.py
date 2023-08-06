import json

from common.variable import common
from settings import mqtt

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