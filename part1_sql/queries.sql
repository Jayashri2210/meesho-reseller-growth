-- Part 1: Meesho Reseller Growth SQL Business Queries

-- 1. Monthly revenue by category
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    CASE category
        WHEN 'Ethnic Wear' THEN 1
        WHEN 'Western Wear' THEN 2
        WHEN 'Kids Wear' THEN 3
        WHEN 'Home & Kitchen' THEN 4
        WHEN 'Beauty & Personal Care' THEN 5
    END;


-- 2. Region-wise total revenue and order count
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;


-- 3. Top resellers by total spend
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;


-- 4a. Resellers who have never placed an order
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;


-- 4b. Demonstration of COUNT(*) versus COUNT(order_id)
-- For an unmatched LEFT JOIN row, COUNT(*) is 1 because
-- the reseller row still exists, while COUNT(order_id) is 0
-- because order_id is NULL.
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS row_count,
    COUNT(o.order_id) AS order_count
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;


-- 5. Average Order Value for June, Delivered orders only
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
