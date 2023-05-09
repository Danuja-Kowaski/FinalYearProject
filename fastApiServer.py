from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import opcode_conv

# connect to MongoDB
mongodb_client = MongoClient("mongodb+srv://user:user@fyp.hcpsniu.mongodb.net/?retryWrites=true&w=majority")
if mongodb_client:
    db = mongodb_client["fyp"]
    contract_collection = db["contracts"]
    users_collection = db["users"]
    test_collection = db["test"]
    model = opcode_conv.load_model()
else:
    print("Unable to load server")

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_KEY = "1485cf41eadade4885fd23caddbac070a9fcfa3f19aabef49cc76927195d4f91"
secret = JWT_KEY
app = FastAPI()

# allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Router functions
@app.post('/login')
async def login(body: dict):
    username = body["username"]
    password = body["password"]
    user_auth = users_collection.find_one({"username": username})
    if user_auth:
        isMatch = pwd_context.verify(password, user_auth['password'])
        if isMatch:
            payload = {"username": user_auth['username']}
            token = jwt.encode(
                payload, secret, algorithm='HS256'
            )
            return {"Token": token}
        else:
            raise HTTPException(
                status_code=401, detail='Invalid username and/or password')
    else:
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')


@app.post("/signup")
async def create_user(body: dict):
    username = body["username"]
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=401, detail='Username already exists')
    email = body["email"]
    password = body["password"]
    hashed_password = pwd_context.hash(password)
    user_data = users_collection.insert_one({"username": username, "email": email, "password": hashed_password})
    if user_data.inserted_id:
        return {"message": "User successfully registered"}
    else:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/contract/predict")
async def predict_contract(body: dict):
    if 'Token' in body:
        username = decode_token(body['Token'])
        contract = body['opcode']
        if contract:
            # opcode = body['opcode']
            # For bytecode conversions
            # opc = convert_to_op(contract)
            result = opcode_conv.run_predictions(model, contract)
            contract_data = contract_collection.insert_one({"contract": contract, "user": username})
            if contract_data:
                return {"message": "Contract added successfully", "result": result}
            else:
                raise HTTPException(status_code=500, detail="Internal server error")
        else:
            raise HTTPException(status_code=400, detail="Cant save contract")


@app.get("/pub/contracts")
async def get_test_contracts():
    contract_data = test_collection.find({})
    contract_list = []
    for contract in contract_data:
        contract_dict = {
            "opcode": contract["opcode"],
        }
        contract_list.append(contract_dict)
        print(contract_list)
    if contract_list:
        return contract_list
    else:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/contract/save")
async def save_contract(body: dict):
    if 'Token' in body:
        username = decode_token(body['Token'])
        usr_contract = body['opcode']
        if usr_contract:
            contract_data = contract_collection.insert_one({"contract": usr_contract, "user": username})
            if contract_data:
                return {"message": "Contract added successfully"}
            else:
                raise HTTPException(status_code=500, detail="Internal server error")
        else:
            raise HTTPException(status_code=400, detail="Cant save contract")


def decode_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid token')

# def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
#     return self.decode_token(auth.credentials)
