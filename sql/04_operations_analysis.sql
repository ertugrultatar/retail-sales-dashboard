-- 1. Order status analysis

SELECT
    order_status,
    COUNT(order_id) AS total_orders,
    ROUND(
        COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM retail_sales),
        2
    ) AS percentage_of_orders
FROM retail_sales
GROUP BY order_status
ORDER BY total_orders DESC;


-- 2. Return rate by product category

SELECT
    product_category,
    COUNT(order_id) AS total_orders,
    SUM(CASE WHEN return_flag = 1 THEN 1 ELSE 0 END) AS returned_orders,
    ROUND(
        SUM(CASE WHEN return_flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id),
        2
    ) AS return_rate_percentage
FROM retail_sales
GROUP BY product_category
ORDER BY return_rate_percentage DESC;


-- 3. Average shipping time by region

SELECT
    region,
    ROUND(AVG(days_to_ship), 2) AS average_shipping_days,
    COUNT(order_id) AS total_orders
FROM retail_sales
GROUP BY region
ORDER BY average_shipping_days DESC;


-- 4. Payment method analysis

SELECT
    payment_method,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales
FROM retail_sales
GROUP BY payment_method
ORDER BY total_sales DESC;