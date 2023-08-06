from pydantic import BaseModel, conint

class Volume(BaseModel):
    volume: conint()

class MotorMovement(BaseModel):
    motor_on_time: conint()
    motor_on_close_time: conint()
    door_hold_time: conint()
    door_open_hold_time: conint()

class CountSet(BaseModel):
    count_set: conint()

class CountMax(BaseModel):
    count_max: conint()

class DoorHoldingPower(BaseModel):
    door_holding_pwm: conint()

class DoorOpenPower(BaseModel):
    door_open_pwm: conint()