import json

from lite_fastapi_local.common.variable import common
from lite_fastapi_local.settings import mqtt

class Motor:

    def send_qr_result(self, qr_code: str, result: str):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/qr_result', json.dumps({
            "qr_code": qr_code,
            "result": result
        }))

    def open_door_force(self, running_time):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "door_open": {
                "duration": str(running_time)
            }
        }))
    
    def close_door_force(self, running_time):
        mac = common.get_MACHINE_MAC()
        mqtt.publish(f'tg/{mac}/control', json.dumps({
            "door_close": {
                "duration": str(running_time)
            }
        }))
        
    
motor = Motor()