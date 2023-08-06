from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from common.variable import common

from model.setupModel import setup
from schema.setupSchema import Volume, MotorMovement, CountMax, CountSet, DoorOpenPower, DoorHoldingPower

router = APIRouter(
    prefix="/setup",
    tags=["setups"],
    responses={404: {"description": "Not found"}}
)

@router.get('/volume')
def change_volume(volume: int):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_volume(volume)
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.get('/motor_movement')
def change_motor_movement(motor_on_time: int, motor_on_close_time: int, door_hold_time: int, door_open_hold_time: int):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_motor_movement(
        motor_on_time=motor_on_time,
        motor_on_close_time=motor_on_close_time,
        door_hold_time=door_hold_time,
        door_open_hold_time=door_open_hold_time
    )
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.get('/count_max')
def change_count_max(count_max: int):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_count_max(count_max)
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.get('/count_set')
def change_count_set(count_set: int):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_count_set(count_set)
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.get('/door_holding_pwm')
def change_door_holding_pwm(door_holding_pwm: int):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_door_holding_pwm(door_holding_pwm)
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)

@router.get('/door_open_pwm')
def change_door_open_pwm(door_open_pwm: int):
    mac = common.get_MACHINE_MAC()
    if not mac:
        content = {
            "code_number": 25,
            "code_name": "no_mac_address",
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    setup.change_door_open_pwm(door_open_pwm)
    content = {
        'code_number': 11, 
        'code_name': 'accepted'
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=content)
