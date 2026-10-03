import pandas as pd
import os
import shutil
import kagglehub
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = 'data_csv'

if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
    print("Downloading data...")
    cache_path= kagglehub.dataset_download("olistbr/brazilian-ecommerce")
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Copying file in the project folder...")
    for file_name in os.listdir(cache_path):
        source_file = os.path.join(cache_path, file_name)
        destination_file = os.path.join(DATA_DIR, file_name)
        if os.path.isfile(source_file):
            shutil.copy(source_file, destination_file)
    print("Data successfully moved to the project folder.")
else:
    print("Data already downloaded in the project folder")

print("Available files: ", os.listdir(DATA_DIR))

customers = pd.read_csv('data_csv/olist_customers_dataset.csv')
geolocation_dataset = pd.read_csv('data_csv/olist_geolocation_dataset.csv')
order_items = pd.read_csv('data_csv/olist_order_items_dataset.csv')
order_payments = pd.read_csv('data_csv/olist_order_payments_dataset.csv')
order_reviews = pd.read_csv('data_csv/olist_order_reviews_dataset.csv')
orders = pd.read_csv('data_csv/olist_orders_dataset.csv')
products = pd.read_csv('data_csv/olist_products_dataset.csv')
sellers = pd.read_csv('data_csv/olist_sellers_dataset.csv')
#product_category_name_transaction = pd.read_csv('data_csv/product_category_name_translation.csv')







