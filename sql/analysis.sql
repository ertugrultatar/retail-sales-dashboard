SELECT *
FROM
retail_sales
LIMIT 10;


- 1. Who are our highest-value customers?
SELECT customer_id, customer_name, SUM(profit) AS total_profit
FROM retail_sales
GROUP BY customer_name, customer_id
ORDER BY total_profit DESC
LIMIT 10;


- Which product categories are driving the most profit?
SELECT product_category, SUM(profit) AS total_profit
FROM retail_sales
GROUP BY product_category
ORDER BY total_profit DESC
LIMIT 10;

- What is our return rate by product category?
SELECT 
    product_category,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN return_flag = 1 THEN 1 ELSE 0 END) AS returned_orders,
    ROUND(
        SUM(CASE WHEN return_flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS return_rate_percentage
FROM retail_sales
GROUP BY product_category
ORDER BY return_rate_percentage DESC;

- Which regions/cities generate the most sales?
SELECT
    region,
    city,
    COUNT(order_id) AS total_orders,
    printf('%,.2f', SUM(sales_amount)) AS total_sales,
    printf('%,.2f', AVG(sales_amount)) AS average_order_value
FROM retail_sales
GROUP BY region, city
ORDER BY SUM(sales_amount) DESC
LIMIT 10;