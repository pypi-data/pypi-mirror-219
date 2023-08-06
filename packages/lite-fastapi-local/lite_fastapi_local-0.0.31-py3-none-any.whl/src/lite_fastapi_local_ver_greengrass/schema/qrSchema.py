from pydantic import constr, BaseModel

class QrCode(BaseModel):
    qr_code: constr()
    move: constr()