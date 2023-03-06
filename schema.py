import re
from typing import Optional

from pydantic import BaseModel, validator
from pydantic import ValidationError

from errors import HttpError


password_regex = re.compile(
    "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
)


class CreateUser(BaseModel):

    username: str
    password: str

    @validator('password')
    def validate_password(cls, value: str):
        if not re.search(password_regex, value):
            raise ValueError('password must contain 8 or more characters')
        else:
            return value


class CreateAdvertisement(BaseModel):

    title: str
    description: Optional[str] = ''


class UpdateAdvertisement(BaseModel):

    title: Optional[str]
    description: Optional[str]


def validate_create_adv(json_data):
    try:
        adv_schema = CreateAdvertisement(**json_data)
        return adv_schema.dict()
    except ValidationError as error:
        raise HttpError(
            status_code=400,
            massage=error.errors()
        )


class Validator:

    def __init__(self, validate_class):
        self.validator = validate_class

    def validate(self, json_data):
        try:
            adv_schema = self.validator(**json_data)
            return adv_schema.dict()
        except ValidationError as error:
            raise HttpError(
                status_code=400,
                massage=error.errors()
            )


validate_update_adv = Validator(UpdateAdvertisement)


def validate_create_user(json_data):
    try:
        user_schema = CreateUser(**json_data)
        return user_schema.dict()
    except ValidationError as error:
        raise HttpError(
            status_code=400,
            massage=error.errors()
        )
