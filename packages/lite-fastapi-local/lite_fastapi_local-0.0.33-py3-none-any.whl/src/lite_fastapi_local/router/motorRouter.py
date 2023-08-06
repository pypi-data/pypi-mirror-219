import asyncio, threading
from datetime import datetime

from fastapi import APIRouter, status, BackgroundTasks
from fastapi.responses import JSONResponse

from common.variable import common
from common.function import capture_image, save_cctv, create_directory

from model.motorModel import motor
from model.ledModel import led
from model.setupModel import setup
from model.sprayModel import spray
from model.boxDoorModel import box_door
from model.solModel import sol

from schema.qrSchema import QrCode

router = APIRouter(
    prefix="/motor",
    tags=["motors"],
    responses={404: {"description": "Not found"}}
)

@router.get("/door")
async def move_door(qr_code: str, move: str, running_time: int, background_tasks: BackgroundTasks):
    common.set_image_directory("")
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    if move == "open":
        common.set_operating_status('opening')
        common.add_returned_qr_code_list(qr_code)
        current_count = common.get_current_count()
        count_max = common.get_count_max()
        # if count_max == current_count:
        #     content = {
        #         "code_number": 23,
        #         "code_name": "unacceptable",
        #     }
        #     return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=content)
        common.set_current_count(current_count + 1)
        setup.change_count_set(current_count + 1)
        datetime_string = datetime.now().strftime("%Y-%m-%d")
        common.set_file_path(datetime_string)
        create_directory(f"Save_file/{datetime_string}/product")
        create_directory(f"Save_file/{datetime_string}/box")
        create_directory(f"Save_file/{datetime_string}/cctv")
        use_inner_camera = common.get_use_inner_camera()
        if use_inner_camera == False:
            capture_image_thread = threading.Thread(target=capture_image)
            capture_image_thread.start()
        use_cctv_camera = common.get_use_cctv_camera()
        if use_cctv_camera == False:
            save_image_thread = threading.Thread(target=save_cctv)
            save_image_thread.start()
            
            # asyncio.create_task(capture_image())
            # asyncio.create_task(save_cctv())
            # background_tasks.add_task(
            #     capture_image
            # )
            # background_tasks.add_task(
            #     save_cctv
            # )
        motor.open_door_force(running_time)
    elif move == "close":
        common.set_operating_status('closing')
        motor.close_door_force(running_time)
    content = {
        "code_number": 11,
        "code_name": "accepted",
        "qr_code": qr_code
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.get("/boxdoor/{power}")
def move_boxdoor(power: str):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    if power == 'on':
        box_door.open_box_door()
    elif power == 'off':
        box_door.close_box_door()
    content = {
        "code_number": 11,
        "code_name": "accepted"
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.get("/led/{power}")
def turn_led(power: str):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    if power == 'on':
        led.turn_on_led()
    elif power == 'off':
        led.turn_off_led()
    content = {
        "code_number": 11,
        "code_name": "accepted",
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.get("/spray/{power}")
def turn_spray(power: str):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    if power == 'on':
        spray.turn_on_spray()
    elif power == 'off':
        spray.turn_off_spray()
    content = {
        "code_number": 11,
        "code_name": "accepted",
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.get("/sol/{index}/{power}")
def turn_spray(index: str, power: str):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    if power == 'on':
        sol.turn_on_sol(str(int(index) - 1))
    elif power == 'off':
        sol.turn_off_sol(str(int(index) - 1))
    content = {
        "code_number": 11,
        "code_name": "accepted",
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)
    