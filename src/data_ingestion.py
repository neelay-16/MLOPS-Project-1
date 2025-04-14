import sys
import os

project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)   # initialise the logger

class DataIngestion:
    def __init__(self,config):    #Constructor
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info("Data Ingestion started with {self.bucket_name} and file is {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.get_bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info("CSV file is successfully downloaded to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error("Error while downloading the CSV file from GCP")
            raise CustomException("Failed to download csv file",e)
        
    def split_data(self):
        try:
            logger.info("Splitting the data into train and test")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size= 1- self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info("Data is successfully split into train and test and saved to respective file paths")

        except Exception as e:
            logger.error("Error while splitting the data")
            raise CustomException("Failed to split the data",e)
        
    def run(self):
        try:
            logger.info("Running the data ingestion")
            self.download_csv_from_gcp()
            self.split_data()
            logger.infor("Data Ingestion completed")
        except Exception as e:
            logger.error("CustomException : {str(ce)}")
            
        finally:
            logger.info("Data Ingestion completed")

if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()