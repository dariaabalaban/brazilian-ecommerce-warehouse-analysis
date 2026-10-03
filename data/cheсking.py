import raw
#
# # 1. Customers Dataset
# print("=== CUSTOMERS DATASET ===")
# # print(raw.customers.shape)
# # print(raw.customers.head())
# print(raw.customers.info())
# # print(raw.customers.describe())
#
#
# # 2. Order Items Dataset
# print("=== ORDER ITEMS DATASET ===")
# # print(raw.order_items.shape)
# # print(raw.order_items.head())
# print(raw.order_items.info())
# # print(raw.order_items.describe())
#
#
# # 3. Order Payments Dataset
# print("=== ORDER PAYMENTS DATASET ===")
# # print(raw.order_payments.shape)
# # print(raw.order_payments.head())
# print(raw.order_payments.info())
# # print(raw.order_payments.describe())
#
#
# # 4. Orders Dataset
# print("=== ORDERS DATASET ===")
# # print(raw.orders.shape)
# # print(raw.orders.head())
# print(raw.orders.info())
# # print(raw.orders.describe())
#
#
# # 5. Products Dataset
# print("=== PRODUCTS DATASET ===")
# # print(raw.products.shape)
# # print(raw.products.head())
# print(raw.products.info())
# print(raw.products.describe())

# print(raw.orders['order_status'].value_counts())

print(raw.customers['customer_state'].unique())
print(raw.orders['order_delivered_customer_date'].sort_values(ascending=False))