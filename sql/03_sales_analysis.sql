-- 1. Top regions and cities by sales

SELECT
    region,
    city,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(AVG(sales_amount), 2) AS average_order_value
FROM retail_sales
GROUP BY region, city
ORDER BY total_sales DESC
LIMIT 10;


-- 2. Monthly sales performance

SELECT
    strftime('%Y-%m', order_date) AS sales_month,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM retail_sales
GROUP BY sales_month
ORDER BY sales_month;


-- 3. Sales performance by product category

SELECT
    product_category,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM retail_sales
GROUP BY product_category
ORDER BY total_sales DESC;