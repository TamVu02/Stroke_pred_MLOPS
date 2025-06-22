import kagglehub
import shutil
import logging

# Create and configure logger
logging.basicConfig(filename="prepare_model.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger('Prepare for model training')
# Setting the threshold of logger to WARNINGS
logger.setLevel(logging.WARNING)

def download_dataset(data_folder):
    # Download latest version
    path = kagglehub.dataset_download("fedesoriano/stroke-prediction-dataset")
    print("Path to dataset files:", path)

    #Move dataset files to data folder
    shutil.move(path, data_folder)
    logger.info(f'Successfully move data to {data_folder}')

if __name__=='__main__':
    logger.info('=== Start setting up ===')
    logger.info('Downloading dataset ...')
    download_dataset('dataset/')
