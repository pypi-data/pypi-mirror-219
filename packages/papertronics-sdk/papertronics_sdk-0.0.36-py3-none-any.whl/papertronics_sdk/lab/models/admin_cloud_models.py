from typing import Optional

from pydantic import BaseModel


class UserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class DeviceRequest(BaseModel):
    name: Optional[str] = None
    number: Optional[int] = None
