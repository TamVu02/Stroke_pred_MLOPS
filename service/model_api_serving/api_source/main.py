import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import logging
from pydantic import BaseModel
import numpy as np
import os
import mlflow
from fastapi import Depends
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
sys.path.append(project_root)

print(sys.path)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Define fastAPI
app = FastAPI()
logger.info('Start running api...')
@app.on_event("startup")
def startup_event():
	logger.info("FastAPI app has started!")

def model_loader():
	#Mlflow settings
	logger.info(f'Mlflow uri: {os.getenv("MLFLOW_TRACKING_URI", "http://172.17.0.1:5001")}')
	mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://172.17.0.1:5001"))  # Docker bridge IP

	REGISTERED_MODEL_NAME = 'stroke_prediction_model'
	STAGE_STATUS = 'Staging'
	MODEL_URI = f"models:/{REGISTERED_MODEL_NAME}/{STAGE_STATUS}"

	logger.info(f'Loading model: {MODEL_URI}')
	model = mlflow.pyfunc.load_model(MODEL_URI)
	logger.info(f'Succesfully load model from {MODEL_URI}')
	return model

class PatientInfo(BaseModel):
	Age: int = 22
	WorkType: str = 'Private'
	Hypertension: int = 0
	HeartDisease: int = 0
	Married: str = 'No'
	Gender: str = 'Female'
	Residence: str = 'Urban'
	Bmi: float = 18.4
	GlucoseLevel: float = 89.6
	Smoking: str = 'never smoked'

	class Config:
		extra = "forbid"

def process_data(data_df):
	data_df['bmi_cat'] = pd.cut(data_df['Bmi'], bins = [0, 23.8, 28.1, 32.8,10000], labels = ['Underweight', 'Ideal', 'Overweight', 'Obesity'])
	data_df['age_cat'] = pd.cut(data_df['Age'], bins = [0,13,18, 45,60,200], labels = ['Children', 'Teens', 'Adults','Mid Adults','Elderly'])
	data_df['avg_glucose_level_cat'] = pd.cut(data_df['GlucoseLevel'], bins = [0,77.245, 114.09, 216.29450000000003, 500], labels = ['Low', 'Normal', 'High', 'Very High'])
	data_df['hypertension_cat'] = data_df['Hypertension'].map({0: 'No', 1: 'Yes'}).astype('category')
	data_df['heart_disease_cat'] = data_df['HeartDisease'].map({0: 'No', 1: 'Yes'}).astype('category')
	data_df = data_df[['Gender','Married', 'WorkType', 'Residence', 'Smoking', 'avg_glucose_level_cat', 'bmi_cat', 'age_cat', 'heart_disease_cat', 'hypertension_cat']]
	data_df.rename(columns={
		'Gender': 'gender',
		'Married': 'ever_married',
		'WorkType': 'work_type',
		'Residence': 'Residence_type',
		'Smoking': 'smoking_status'
	}, inplace=True)
	for col in data_df.columns:
		data_df[col] = data_df[col].astype(str)
	return data_df

#Define end point
@app.post("/predict")
def predict(data: PatientInfo, model = Depends(model_loader)):
	logger.info("Make predictions...")
	logger.info(data)

	#data processing to match with model input format
	logger.info('Start process data')
	try:
		input_data = process_data(pd.DataFrame(jsonable_encoder(data), index=[0]))
		logger.info(f"Finish process data: {input_data}")
	except Exception as e:
		raise HTTPException(status_code=422, detail=str(e))
	
	# Convert data to pandas DataFrame and make predictions
	logger.info('Start predictions')
	try:
		pred = model.predict(input_data)[0]
		logger.info(f'Model return prediction = {pred}')
	except Exception as e:
		print(e)

	# Return the result
	return {"stroke": int(pred)}
