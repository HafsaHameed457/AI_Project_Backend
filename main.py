from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import JSONResponse
from routes import heart_prediction
from fastapi.middleware.cors import CORSMiddleware

from models.global_models import GETKEY, MyResponse


from controllers.rsa_encryption import generate_and_store_rsa_keys, get_rsa_public_key
from controllers.aes_encryption import generate_aes_key



# create tables



app = FastAPI()


@app.on_event("startup")
async def server():
    await generate_and_store_rsa_keys()
    await generate_aes_key()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(heart_prediction.router, prefix="/api/files")



@app.get("/")
async def welcome():
    public_key = await get_rsa_public_key()

    response_content = MyResponse(
        success=True,
        error="",
        message="AirVault - Elevating security, defying compromise.",
        content={"public_key": public_key},
    )
    return JSONResponse(content=response_content.dict(), status_code=200)
