-- ***************************** KPI *****************************
 
--  1. Total Revenue
SELECT ROUND(SUM(total_price),2) as Total_Revenue from pizza_sales;

-- 2. Average Order Value
SELECT ROUND(SUM(total_price)/COUNT(distinct(order_id)),2) AS Avg_Amt_per_Order FROM pizza_sales;

-- 3. Total Pizza Sold
SELECT SUM(quantity) AS Total_Pizza_Sold FROM pizza_sales;

-- 4. Total Order Placed
SELECT COUNT(DISTINCT(order_id)) AS Total_Order_Placed FROM pizza_sales;

-- 5. Average Pizza Per Order
 SELECT ROUND(SUM(quantity)/COUNT(DISTINCT(order_id)),2) AS Avg_Pizza_per_Order FROM pizza_sales;

-- **************************** Chart Req *****************************

-- 1. Bar chart on Daily basis (Mon,...Sun)
SELECT DAYNAME(STR_TO_DATE(order_date,'%d-%m-%YYYY')) AS Days, COUNT(DISTINCT(order_id)) AS Total_Orders FROM pizza_sales
GROUP BY Days;

-- 2. line chart on Mothly basis (Jan,...Dec)
SELECT MONTHNAME(STR_TO_DATE(order_date,'%d-%m-%YYYY')) AS Months, COUNT(DISTINCT(order_id)) AS Total_Orders FROM pizza_sales
GROUP BY Months;

-- 3. Percentage of Sales by Pizza Category
SELECT DISTINCT(pizza_category), ROUND(SUM(total_price),2) AS Total_Sales, ROUND(SUM(total_price)*100/(SELECT SUM(total_price) FROM pizza_sales),2) AS Sales_in_Percent FROM pizza_sales
GROUP BY pizza_category;

-- 4. Percentage of sales by Pizza size.
SELECT DISTINCT(pizza_size), ROUND(SUM(total_price),2) AS Total_Sales, ROUND(SUM(total_price)*100/(SELECT SUM(total_price) FROM pizza_sales),2) AS Sales_in_Percent FROM pizza_sales
GROUP BY pizza_size;

-- 5. Total Pizza Sold by Pizza Category.
SELECT DISTINCT(pizza_category), ROUND(SUM(total_price),2) AS Total_Sales, ROUND(SUM(total_price)*100/(SELECT SUM(total_price) FROM pizza_sales),2) AS Sales_in_Percent FROM pizza_sales
GROUP BY pizza_category;

-- 5.1. Hourly Basis per Day
SELECT HOUR(order_time) AS order_time, COUNT(DISTINCT(order_id)) AS Total_Orders FROM pizza_sales
GROUP BY HOUR(order_time);

-- 6.1 Top5 Best Pizza by Revenue.
SELECT pizza_name, SUM(total_price) AS Total_Price FROM pizza_sales
GROUP BY pizza_name ORDER BY Total_Price DESC LIMIT 5;


-- 6.2 Top5 Best Pizza by Total Quantity.
SELECT pizza_name, SUM(quantity) AS Total_Quantity FROM pizza_sales
GROUP BY pizza_name ORDER BY Total_Quantity DESC LIMIT 5;

-- 6.3 Top5 Best Pizza by Total Orders.
SELECT pizza_name, COUNT(DISTINCT(order_id)) AS Total_Orders FROM pizza_sales
GROUP BY pizza_name ORDER BY Total_Orders DESC LIMIT 5;


-- 7.1 Bottom 5 Worst Pizza by Revenue.
SELECT pizza_name, SUM(total_price) AS Total_Price FROM pizza_sales
GROUP BY pizza_name ORDER BY Total_Price ASC LIMIT 5;

-- 7.2 Bottom 5 Worst Pizza by Total Quantity.
SELECT pizza_name, SUM(quantity) AS Total_Quantity FROM pizza_sales
GROUP BY pizza_name ORDER BY Total_Quantity ASC LIMIT 5;

-- 7.3 Bottom 5 Worst Pizza by Total Orders.
SELECT pizza_name, COUNT(DISTINCT(order_id)) AS Total_Orders FROM pizza_sales
GROUP BY pizza_name ORDER BY Total_Orders ASC LIMIT 5;

select * from pizza_sales;


select count(*) from pizza_sales ;
