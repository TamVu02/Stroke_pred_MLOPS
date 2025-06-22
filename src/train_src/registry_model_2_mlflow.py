import mlflow
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient

import io
from datetime import datetime
from PIL import Image

from catboost import CatBoostClassifier, Pool
import numpy as np
import pandas as pd
import joblib
from sklearn import metrics
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTEN

#MLFLOW
MLFLOW_URI = "http://localhost:5001"
MLFLOW_TAG = 'Training Info'
MLFLOW_TAG_DESC = "Training for Stroke prediction model"
MLFLOW_EXPERIMENT_NAME = 'Stroke prediction'

#MLFLOW MODEL
MODEL_NAME = 'stroke_pred_model'
REGISTERED_MODEL_NAME = 'stroke_prediction_model'
MODEL_TAG = 'validation_status' #approved/ required validation
MODEL_ALIAS = 'champion'
METRICS_NAME = 'Balanced Accuracy'
METRICS_THRES = 0.7

#MODEL & DATA PARAMS
SEED = 42
BASE_PATH = '/home/tamvlb/VSCode_projects_work/MLOPs_K5_Capstone'
PROCESSED_DATA_PATH = '/dataset/processed_data/processed_stroke_data.csv'

# Create a new MLflow Experiment/ Set Experiment
mlflow.set_tracking_uri(MLFLOW_URI)
mlflow.autolog()
client = MlflowClient()
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
mlflow_run_name=f'training_{MODEL_NAME}_{datetime.now()}'

#Start an Mlflow run
with mlflow.start_run(run_name=mlflow_run_name) as run:
	print('Connect to mlflow. Start doing experiments now')
	
	mlflow.set_tag(MLFLOW_TAG, MLFLOW_TAG_DESC)

	'''
	----------------------------- PREPARE DATA -----------------------------
	'''
    # READ DATA
	data_df = pd.read_csv(BASE_PATH+PROCESSED_DATA_PATH)
	#data_df = data_df.sample(frac=1).reset_index(drop=True)
	label_col = 'stroke'
	feat_col = [col for col in data_df.columns if col != label_col]
	print(data_df.columns)
	
    # SPLIT DATA TRAIN VAL TEST
	X_data = data_df[feat_col]
	y_data = data_df[label_col]
	print(X_data.shape, y_data.shape)
	X_train, X_val, y_train, y_val = train_test_split(X_data, y_data, test_size=0.25, random_state=SEED) 
	X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, test_size=0.1/0.25, random_state=SEED)
	print(f'Train data shape: {X_train.shape}, validate data shape: {X_val.shape}, test data shape: {X_test.shape}')
	print(f'Label count in train data: {y_train.value_counts(normalize=True)}, validate data: {y_val.value_counts(normalize=True)}, test data: {y_test.value_counts(normalize=True)}')
	print(f'Feature data sample: {X_train.head(3)}')
	assert X_train.shape[0] + X_val.shape[0] + X_test.shape[0] == X_data.shape[0]
	
    # SMOTEN DATA SAMPLING
	smote = SMOTEN()
	X_resample, y_resample = smote.fit_resample(X_train, y_train)
	print(f'Training data after resample: {X_resample.shape}')

	# SAVE MLFLOW DATA SIGNATURE
	signature = infer_signature(X_test, y_test)
	
	# CREATE POOL DATA
	train_data = Pool(X_resample, y_resample, cat_features=feat_col)
	val_data = Pool(X_val, y_val, cat_features=feat_col)
	test_data = Pool(X_test, y_test, cat_features=feat_col)

	'''
	----------------------------- START TRAINING MODEL -----------------------------
	'''
	# MLFLOW LOG MODEL NAME
	mlflow.log_param('model_name',f'CatBoost {MODEL_NAME}')

	#DEFINE MODEL PARAMS
	best_para = {'learning_rate': 0.0852624, 
			  'iterations': 45, 
			  'max_depth': 3, 
			  'l2_leaf_reg': 6, 
			  'subsample': 0.7839244, 
			  'od_pval': 0.05961997552765307, 
			  'od_wait': 12,
			  'od_type':'Iter', 
			  'eval_metric':'BalancedAccuracy', 
			  'loss_function':'CrossEntropy', 
			  'bootstrap_type' : 'Bernoulli', 
			  'verbose' : 500}
	print(best_para)

	#MLFLOW LOG MODEL PARAMS
	for k,v in best_para.items():
		mlflow.log_param(k,v)

	# TRAINING MODEL
	model_cls = CatBoostClassifier(**best_para)
	model_cls.fit(train_data, eval_set=val_data, early_stopping_rounds=50)

	# MLFLOW LOG MODEL
	model_info = mlflow.catboost.log_model(
		model_cls,
		MODEL_NAME,
		signature = signature,
		input_example=X_test
	)

	# MLFLOW LOG MODEL TRAINING HISTORY
	metrics_model = model_cls.get_evals_result()
	for i in range (best_para['iterations']):
		mlflow.log_metric('train_logloss',metrics_model['learn'][best_para['loss_function']][i], step=i)
		mlflow.log_metric('val_logloss',metrics_model['validation'][best_para['loss_function']][i], step=i)

	# MLFLOW REGISTRY MODEL
	model_uri = model_info.model_uri
	registered_model = mlflow.register_model(model_uri=model_uri, name=REGISTERED_MODEL_NAME)
	cur_model_ver = registered_model.version

	'''
	----------------------------- MODEL VALIDATION -----------------------------
	'''
	# MODEL'S PREDICTION ON TEST SET
	y_pred = model_cls.predict(X_test)
	cf_mat=metrics.confusion_matrix(y_test, y_pred)
	cf_mat=cf_mat/cf_mat.astype(np.float64).sum(axis=1)
	cf_mat_display=metrics.ConfusionMatrixDisplay(cf_mat)
	cf_mat_display.plot()

	buffer_image = io.BytesIO()
	plt.gcf().savefig(buffer_image, format='png')
	buffer_image.seek(0)
	mlflow.log_image(Image.open(buffer_image),'plots/cfmat_stroke_pred.png')
	plt.close()

	# MLFLOW LOG MODEL METRIC ON TEST SET
	b_acc = metrics.balanced_accuracy_score(y_test, y_pred)
	mlflow.log_metric(METRICS_NAME, b_acc)
	metrics = model_cls.get_evals_result()

	# MLFLOW SET STAGES
	if b_acc >= METRICS_THRES:
		client.transition_model_version_stage(
		name=REGISTERED_MODEL_NAME,
		version=cur_model_ver,
		stage="Staging"
	)
			
mlflow.end_run()        
print('FINISHED')
