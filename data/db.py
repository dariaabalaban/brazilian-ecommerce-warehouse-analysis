#Saving to db
from pathlib import Path
import data.raw as raw
import sqlite3
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent

conn = sqlite3.connect(DATA_DIR/'olist.db')
category_mapping = pd.read_csv(DATA_DIR/'category_mapping.csv')
category_mapping.to_sql('category_mapping', conn, if_exists = 'replace', index = False)
raw.orders.to_sql('orders', conn, if_exists = 'replace', index = False)
raw.order_items.to_sql('order_items', conn, if_exists = 'replace', index = False)
raw.products.to_sql('products', conn, if_exists = 'replace', index = False)
raw.customers.to_sql('customers', conn, if_exists = 'replace', index = False)
raw.sellers.to_sql('sellers', conn, if_exists = 'replace', index = False)
