from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

OAuth2Dep = Annotated[OAuth2PasswordRequestForm, Depends()]
