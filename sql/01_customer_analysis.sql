-- 1. Top 10 customers by total spending

SELECT
    customer_id,
    customer_name,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_spent,
    ROUND(AVG(sales_amount), 2) AS average_order_value
FROM retail_sales
GROUP BY customer_id, customer_name
ORDER BY total_spent DESC
LIMIT 10;


-- 2. Customer satisfaction analysis

SELECT
    customer_satisfaction,
    COUNT(order_id) AS total_orders,
    ROUND(AVG(sales_amount), 2) AS average_spend
FROM retail_sales
GROUP BY customer_satisfaction
ORDER BY customer_satisfaction DESC;


-- 3. Sales by customer gender

SELECT
    gender,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(AVG(sales_amount), 2) AS average_order_value
FROM retail_sales
GROUP BY gender
ORDER BY total_sales DESC;


-- 4. Customers with returned orders

SELECT
    customer_name,
    COUNT(order_id) AS returned_orders,
    ROUND(SUM(sales_amount), 2) AS returned_sales
FROM retail_sales
WHERE return_flag = 1
GROUP BY customer_name
ORDER BY returned_sales DESC
LIMIT 10;