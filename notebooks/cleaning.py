import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import data.raw as raw

raw.products['product_category_name'] = raw.products['product_category_name'].fillna('Unknown')
raw.products['product_photos_qty'] = raw.products['product_photos_qty'].fillna(0)
raw.products.to_csv('../data/processed.csv/products_clean.csv', index = False)
print(raw.products['product_category_name'].isna().sum())
print(raw.products['product_photos_qty'].isna().sum())
#data in this column is written in the ideal international standard(ISO 8601) so it is no need to write a format
raw.order_items['shipping_limit_date'] = pd.to_datetime(raw.order_items['shipping_limit_date'])


columns = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

for col in columns:
    raw.orders[col] = pd.to_datetime(raw.orders[col])



raw.products['product_category_name'] = raw.products['product_category_name'].replace(r'_2$', '', regex = True)
#print(raw.products['product_category_name'].value_counts().sort_index())
warning = raw.orders[(raw.orders['order_status'] == 'delivered') & (raw.orders['order_approved_at'].isna())]
print(len(warning))

