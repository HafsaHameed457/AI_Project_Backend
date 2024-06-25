from fastapi import APIRouter, Header, Request, Form

router = APIRouter()
from fastapi.responses import JSONResponse
from models.global_models import MyResponse
from controllers.rsa_encryption import decrypt_from_rsa_private_key
from controllers.heart_prediction import predict_heart_disease
from typing import Any, List

from urllib.parse import unquote


@router.post("/predict")
async def predict_heart(
Age: str=Form(...),
       Sex: str=Form(...),
        ChestPainType: str=Form(...),
            RestingBloodPressure: str=Form(...),
            SerumCholestoral: str=Form(...),
            FastingBloodSugar: str=Form(...),
            RestingElectrocardiographicResults: str=Form(...),
            MaximumHeartRateAchieved: str=Form(...),
            ExerciseInducedAngina: str=Form(...),
            Oldpeak: str=Form(...),
            Slope: str=Form(...),
            public_key: str = Header(...),

):
    try:
        ChestPainType=await decrypt_from_rsa_private_key(ChestPainType)
        Age=await decrypt_from_rsa_private_key(Age)
        RestingBloodPressure=await decrypt_from_rsa_private_key(RestingBloodPressure)
        SerumCholestoral=await decrypt_from_rsa_private_key(SerumCholestoral)
        FastingBloodSugar=await decrypt_from_rsa_private_key(FastingBloodSugar)
        RestingElectrocardiographicResults=await decrypt_from_rsa_private_key(RestingElectrocardiographicResults)
        MaximumHeartRateAchieved=await decrypt_from_rsa_private_key(MaximumHeartRateAchieved)
        ExerciseInducedAngina=await decrypt_from_rsa_private_key(ExerciseInducedAngina)
        Oldpeak=await decrypt_from_rsa_private_key(Oldpeak)
        Slope=await decrypt_from_rsa_private_key(Slope)

        response=await predict_heart_disease(
            Age,
            Sex,
            ChestPainType,
            RestingBloodPressure,
            SerumCholestoral,
            FastingBloodSugar,
            RestingElectrocardiographicResults,
            MaximumHeartRateAchieved,
            ExerciseInducedAngina,
            Oldpeak,
            Slope,
            public_key
        )


        return response
    except Exception as e:
        print(e)
        response_content = MyResponse(
            success=False,
            error="Couldn't search for keywords",
            message="",
            content={},
        )
        return JSONResponse(content=response_content.dict(), status_code=500)
