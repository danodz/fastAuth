from fastapi import Request, FastAPI, Response, HTTPException
from pydantic import BaseModel
import db
import bcrypt
from uuid import uuid4
import jwt
import json
from fpdf import FPDF

app = FastAPI()

class NewUser(BaseModel):
    username:str
    password:str
    firstname:str
    lastname:str

class UserAuthRequest(BaseModel):
    username:str
    password:str

@app.post("/signup")
def signupHandler(user:NewUser):
    _id = uuid4()
    db.usersCreds.insert_one({
        "username" : user.username,
        "password" : bcrypt.hashpw(user.password.encode("utf8"), bcrypt.gensalt()),
        "userId" : _id
    })
    db.users.insert_one({
        "_id": _id,
        "username" : user.username,
        "firstname" : user.firstname,
        "lastname" : user.lastname
    })
    return {}

@app.post("/authenticate")
def authHandler(credentials:UserAuthRequest):
    user = db.usersCreds.find_one({"username":credentials.username})
    raise HTTPException(status_code=401, detail="Wrong password or user")
    if bcrypt.checkpw(credentials.password.encode(), user["password"]):
        return {"jwt": jwt.encode({"Authenticated":True}, "secret", algorithm="HS256")}
    else:
        raise HTTPException(status_code=401, detail="Wrong password or user")

def getAllUsers():
    return list(db.users.find())

def getUsersAsPDF():
    users = getAllUsers()
    pdf = FPDF('p', 'mm', 'a4')
    pdf.set_font('Arial', 'B', 16)
    pdf.add_page()
    for user in users:
        pdf.cell(40, 10, user["username"] + ": " + user["firstname"] + " " + user["lastname"], 0, 1)
    return pdf.output(dest='S').encode('latin-1')

@app.get("/users")
def usersHandler(request:Request):
    params = dict(request.query_params)
    if("jwt" in params):
        try:
            jwt.decode(params["jwt"], "secret", algorithms=["HS256"])
        except:
            raise HTTPException(status_code=403, detail="You are not correctly logged in")
    else:
        raise HTTPException(status_code=403, detail="You are not logged in")
        
    if("filter" in params):
        return db.users.find_one(json.loads(params["filter"]))
    elif("download" in params and params["download"] == "pdf"):
        return Response(getUsersAsPDF(), media_type='application/pdf')
    else:
        return {"users": getAllUsers()}

def dbReset():
    users = [
        NewUser(
            username= "user",
            password= "pass",
            firstname= "User",
            lastname= "Name"
        ),
        NewUser(
            username= "erwan",
            password= "password",
            firstname= "Erwan",
            lastname= "LeBlanc"
        ),
        NewUser(
            username= "sid",
            password= "pw",
            firstname= "Sid",
            lastname= "Benachenhou"
        ),
        NewUser(
            username= "admin",
            password= "adminadmin",
            firstname= "Administrator",
            lastname= "Administrating"
        ),
        NewUser(
            username= "doctor",
            password= "river",
            firstname= "John",
            lastname= "Smith"
        ) 
    ]
    for user in users:
        signupHandler(user)
#dbReset()
