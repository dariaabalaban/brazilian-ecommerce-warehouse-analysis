import pandas as pd
import data.db as db

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

#number of cancellations by category
query = """
    WITH base AS(
        SELECT 
            c.macro_category, 
            o.order_id,
            o.order_status,
            SUM(i.price) AS total_price,
            SUM(i.freight_value) AS total_freight
        FROM orders o
        JOIN order_items i ON o.order_id = i.order_id
        JOIN products p ON i.product_id  = p.product_id
        JOIN category_mapping c ON p.product_category_name = c.product_category_name
        WHERE o.order_status IN ('delivered', 'canceled')
        GROUP BY c.macro_category, o.order_id, o.order_status
    )
    SELECT 
        macro_category, 
        SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) as canceled_orders,
        ROUND(CAST(SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) AS FLOAT)/COUNT(DISTINCT order_id) * 100.0, 2) AS cancel_rate_pct,
        ROUND(AVG(total_price), 2) AS avg_price,
        ROUND(AVG(total_freight), 2) AS avg_freight,
        ROUND(AVG(total_freight/total_price * 100.0), 2) AS avg_freight_ratio_pct
    FROM base
    GROUP BY macro_category
    ORDER BY avg_freight_ratio_pct DESC;
"""

category_freight_stats = pd.read_sql(query, db.conn)
print(category_freight_stats)

print('---' * 40)
print('\nwarehouse problems ')

#Delivery time by state
query = """
    WITH base AS(
        SELECT
            o.order_id,
            c.customer_state,
            SUM(i.freight_value) As total_freight,
            ROUND(JULIANDAY(o.order_delivered_customer_date) - JULIANDAY(o.order_purchase_timestamp) , 2) AS delivery_days
            FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        JOIN order_items i ON o.order_id = i.order_id
        WHERE o.order_status = 'delivered'
        AND o.order_delivered_customer_date IS NOT NULL
        GROUP BY o.order_id, c.customer_state
    )
    SELECT
        customer_state,
        COUNT(order_id) AS total_orders,
        ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
        ROUND(COUNT(order_id) * 100.0 / SUM(COUNT(order_id)) OVER(), 2) AS order_share_pct,
        ROUND(AVG(total_freight), 2) AS avg_freight,
        ROUND(SUM(total_freight), 2) AS total_freight
    FROM base
    GROUP BY customer_state
    ORDER BY total_orders DESC;

"""
delivery_by_state = pd.read_sql(query, db.conn)
print(delivery_by_state)



#cancellation rate by state
query = """
    WITH base AS(
        SELECT
            c.customer_state,
            o.order_id,
            o.order_status,
            SUM(i.price) AS total_price,
            SUM(i.freight_value) AS total_freight
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        JOIN order_items i On o.order_id = i.order_id
        WHERE o.order_status IN ('delivered', 'canceled')
        GROUP BY c.customer_state, o.order_id, o.order_status
    )
    SELECT
        customer_state,
        SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) as canceled_orders,
        ROUND(CAST(SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT order_id) * 100.0, 2) AS cancel_rate_pct,
        ROUND(AVG(total_price), 2) AS avg_price,
        ROUND(AVG(total_freight), 2) AS avg_freight,
        ROUND(AVG(total_freight/total_price * 100.0), 2) AS avg_freight_ratio_pct
    FROM base
    GROUP BY customer_state
    ORDER BY avg_freight_ratio_pct DESC;

"""
cancellations_by_state = pd.read_sql(query, db.conn)
print(cancellations_by_state)


#Delivery growth by state
query = """
    WITH base AS(
        SELECT
            c.customer_state,
            SUM(CASE WHEN STRFTIME( '%Y', o.order_delivered_customer_date) = '2017'
                AND STRFTIME('%m',o.order_delivered_customer_date) <= '09' THEN 1 ELSE 0 END) AS orders_2017,
            SUM(CASE WHEN STRFTIME( '%Y', o.order_delivered_customer_date) = '2018'
                AND STRFTIME('%m',o.order_delivered_customer_date) <= '09' THEN 1 ELSE 0 END) AS orders_2018
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        WHERE o.order_status = 'delivered'
        AND o.order_delivered_customer_date IS NOT NULL
        GROUP BY c.customer_state
    )
    SELECT
        customer_state,
        orders_2017,
        orders_2018,
        (orders_2018 - orders_2017) AS absolute_growth,
        ROUND((CAST(orders_2018 AS FLOAT) - orders_2017)/NULLIF(orders_2017, 0) * 100, 2) AS increase_pct
    FROM base
    WHERE orders_2017 > 0
    ORDER BY absolute_growth DESC;

"""

growth_by_state = pd.read_sql(query, db.conn)
print(growth_by_state)



