import serial

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from common.variable import common

router = APIRouter(
    prefix="/sensor",
    tags=["sensors"],
    responses={404: {"description": "Not found"}}
)

@router.get("/lidar")
def find_lidar_sensor_depth():
    port = common.get_lidar_sensor_port()
    if not port:
        content = {
            "code_number": 26,
            "code_name": "no_port"
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    ser = serial.Serial(port,115200,timeout = 1)
    data = ser.read(9)
    if data[0] == 0x59 and data[1] == 0x59: # 데이터의 첫 두 바이트가 0x59인지 확인합니다.
        distance = data[2] + data[3] * 256
        content = {
            "code_number": 10,
            "code_name": "success",
            "distance": distance,
            "unit": "cm"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    