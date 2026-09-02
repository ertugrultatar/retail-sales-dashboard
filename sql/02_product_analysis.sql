-- 1. Best-selling product categories by revenue

SELECT
    product_category,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM retail_sales
GROUP BY product_category
ORDER BY total_sales DESC;


-- 2. Most profitable products

SELECT
    product_name,
    product_category,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS units_sold
FROM retail_sales
GROUP BY product_name, product_category
ORDER BY total_profit DESC
LIMIT 10;


-- 3. Top products by quantity sold

SELECT
    product_name,
    product_category,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales_amount), 2) AS total_sales
FROM retail_sales
GROUP BY product_name, product_category
ORDER BY total_units_sold DESC
LIMIT 10;


-- 4. Products with highest return rates

SELECT
    product_name,
    product_category,
    COUNT(order_id) AS total_orders,
    SUM(CASE WHEN return_flag = 1 THEN 1 ELSE 0 END) AS returned_orders,
    ROUND(
        SUM(CASE WHEN return_flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id),
        2
    ) AS return_rate_percentage
FROM retail_sales
GROUP BY product_name, product_category
HAVING total_orders >= 5
ORDER BY return_rate_percentage DESC
LIMIT 10;