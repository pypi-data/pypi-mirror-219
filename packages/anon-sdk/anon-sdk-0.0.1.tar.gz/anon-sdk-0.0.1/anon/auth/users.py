from logging import getLogger

import anon.client
from anon.exceptions import InvalidCredentials, InvalidIdError
import anon.basemodel
from pydantic import BaseModel
from typing import Optional


logger = getLogger(__name__)

class _UserEmail(BaseModel):
   verified: bool
   value: str 

class User(anon.basemodel.AnonBase):
    """A Login User.
    Raises InvalidCredentials if login failed or not able to fetch rsk or token.
    """

    name: str
    email: _UserEmail
    role: str
    user_id: str
    # organization_id: str
    root_secret_key:Optional[str]

    @classmethod
    def from_login(cls, email: str, password: str, client: "anon.client.BaseClient")->"User": #type: ignore
        res = client.session.post(
            client.infer_url.rstrip('/')+"/users/login",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"},
        )
        if res.status_code > 200:
            raise InvalidCredentials(res.text)
        return cls(**res.json()['data'])
    
    @classmethod
    def from_user_id(cls, user_id:str, client: "anon.client.BaseClient") -> "User":
        res = client.get(
            "/users",
            {"userId": user_id},
        )
        if res.status_code > 200:
            raise InvalidIdError(res.text)
        return cls(**res.json()['data']['users'][0])
