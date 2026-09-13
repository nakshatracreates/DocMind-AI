from pydantic import BaseModel,EmailStr

class usercreate(BaseModel):
    email:EmailStr
    password:str

class userlogin(BaseModel):
    email: EmailStr
    password: str

class questionrequest(BaseModel):
    question:str
    