




from fastapi.encoders import jsonable_encoder


import base64
from controllers.rsa_encryption import encrypt_from_rsa_public_key_string
from fastapi.responses import JSONResponse
from models.global_models import MyResponse 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
async def predict_heart_disease(
       Age: str,
       Sex: str,
        ChestPainType: str,
            RestingBloodPressure: str,
            SerumCholestoral: str,
            FastingBloodSugar: str,
            RestingElectrocardiographicResults: str,
            MaximumHeartRateAchieved: str,
            ExerciseInducedAngina: str,
            Oldpeak: str,
            Slope: str,

):
    try:

        data = pd.read_csv("heart.csv")
        objcol = [col for col in data.columns if data[col].dtype == 'object']
        numcol = [col for col in data.columns if data[col].dtype != 'object']
        label_encoder = LabelEncoder()
        for col in objcol:
            data[col] = label_encoder.fit_transform(data[col])


        heart=data['HeartDisease']
        targetdata = data.drop('HeartDisease',axis = 'columns')


        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(targetdata)
        data_scaled = pd.DataFrame(data_scaled, columns=targetdata.columns)



        corr = data_scaled.corr()
        plt.figure(figsize=(16,6))
        mask =np.triu(np.ones_like(corr, dtype=bool))
        heatmap=sns.heatmap(corr,mask=mask,cmap='YlGnBu', vmin=-1, vmax= 1 , center=0, annot=True,linewidth=.5,square=False);
        heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12)
        # plt.show()

        print(data_scaled)

        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > 0.5)]
        data_scaled.drop(to_drop, axis=1, inplace=True)
        x_selected = data_scaled
        y = heart

        x_train, x_test, y_train, y_test = train_test_split(x_selected,y, test_size=0.2, random_state = 42)

        lr=LogisticRegression()
        lr.fit(x_train,y_train)
        y_pred_lr=lr.predict(x_test)
        lr_accuracy=accuracy_score(y_test,y_pred_lr)
        lr_precision = precision_score(y_test,y_pred_lr)
        lr_recall = recall_score(y_test,y_pred_lr)
        lr_f1= f1_score(y_test,y_pred_lr)

        print('Accuracy is :', lr_accuracy)
        print('Precision is :', lr_precision)
        print('Recall is :', lr_recall)
        print('F1 Score is :', lr_f1)
        new_data=(Age, Sex,ChestPainType,RestingBloodPressure, SerumCholestoral, FastingBloodSugar, RestingElectrocardiographicResults, MaximumHeartRateAchieved, ExerciseInducedAngina, Oldpeak, Slope)
        new_data_df = pd.DataFrame([new_data], columns=targetdata.columns)
        print(new_data_df)
        for col in objcol:
            new_data_df[col] = label_encoder.fit_transform(new_data_df[col])

        # Scaling the data
        data_scaled = scaler.fit_transform(new_data_df)
        data_scaled = pd.DataFrame(data_scaled, columns=targetdata.columns)


        # Predict the value
        predicted_value = lr.predict(data_scaled)

        # Print the prediction

        response_content = MyResponse(
            success=True,
            error="",
            message="Heart Disease Prediction",
            content={"Predicted Value": "Heart Disease" if predicted_value[0] else "No Heart Disease" },
        )
        return JSONResponse(content=response_content.dict(), status_code=200)
    except Exception as e:
        print(e)
        response_content = MyResponse(
            success=False,
            error="Couldn't predict the disease.",
            message="",
            content={},
        )
        return JSONResponse(content=response_content.dict(), status_code=500)
