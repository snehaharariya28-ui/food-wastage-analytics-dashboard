-- LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
-- SQL Queries for Analysis

-- Query 1: Count of providers and receivers per city
SELECT 
    p.City,
    COUNT(DISTINCT p.Provider_ID) AS Total_Providers,
    COUNT(DISTINCT r.Receiver_ID) AS Total_Receivers
FROM providers p
LEFT JOIN receivers r ON p.City = r.City
GROUP BY p.City
ORDER BY Total_Providers DESC;


-- Query 2: Which provider type contributes the most food?
SELECT 
    Provider_Type,
    COUNT(*) AS Total_Listings,
    SUM(Quantity) AS Total_Quantity
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC;


-- Query 3: Contact information of food providers in a specific city
SELECT 
    Name,
    Type,
    Address,
    City,
    Contact
FROM providers
WHERE City = 'New Carol'
ORDER BY Name;


-- Query 4: Which receivers have claimed the most food?
SELECT 
    r.Name,
    r.Type,
    r.City,
    COUNT(c.Claim_ID) AS Total_Claims
FROM receivers r
JOIN claims c ON r.Receiver_ID = c.Receiver_ID
GROUP BY r.Name, r.Type, r.City
ORDER BY Total_Claims DESC
LIMIT 10;


-- Query 5: Total quantity of food available from all providers
SELECT 
    SUM(Quantity) AS Total_Food_Available,
    COUNT(*) AS Total_Listings,
    ROUND(AVG(Quantity), 2) AS Avg_Quantity_Per_Listing
FROM food_listings;


-- Query 6: Which city has the highest number of food listings?
SELECT 
    Location AS City,
    COUNT(*) AS Total_Listings,
    SUM(Quantity) AS Total_Quantity
FROM food_listings
GROUP BY Location
ORDER BY Total_Listings DESC
LIMIT 10;


-- Query 7: Most commonly available food types
SELECT 
    Food_Type,
    COUNT(*) AS Total_Listings,
    SUM(Quantity) AS Total_Quantity,
    ROUND(AVG(Quantity), 2) AS Avg_Quantity
FROM food_listings
GROUP BY Food_Type
ORDER BY Total_Listings DESC;


-- Query 8: How many food claims have been made for each food item?
SELECT 
    fl.Food_Name,
    fl.Food_Type,
    fl.Meal_Type,
    COUNT(c.Claim_ID) AS Total_Claims
FROM food_listings fl
LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
GROUP BY fl.Food_Name, fl.Food_Type, fl.Meal_Type
ORDER BY Total_Claims DESC
LIMIT 10;


-- Query 9: Which provider has had the highest number of successful claims?
SELECT 
    p.Name AS Provider_Name,
    p.Type AS Provider_Type,
    p.City,
    COUNT(c.Claim_ID) AS Successful_Claims
FROM providers p
JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
JOIN claims c ON fl.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name, p.Type, p.City
ORDER BY Successful_Claims DESC
LIMIT 10;


-- Query 10: Percentage of claims by status
SELECT 
    Status,
    COUNT(*) AS Total_Claims,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
FROM claims
GROUP BY Status
ORDER BY Percentage DESC;


-- Query 11: Average quantity of food claimed per receiver
SELECT 
    r.Name AS Receiver_Name,
    r.Type AS Receiver_Type,
    COUNT(c.Claim_ID) AS Total_Claims,
    ROUND(AVG(fl.Quantity), 2) AS Avg_Quantity_Per_Claim
FROM receivers r
JOIN claims c ON r.Receiver_ID = c.Receiver_ID
JOIN food_listings fl ON c.Food_ID = fl.Food_ID
GROUP BY r.Name, r.Type
ORDER BY Avg_Quantity_Per_Claim DESC
LIMIT 10;


-- Query 12: Which meal type is claimed the most?
SELECT 
    fl.Meal_Type,
    COUNT(c.Claim_ID) AS Total_Claims,
    SUM(fl.Quantity) AS Total_Quantity
FROM food_listings fl
JOIN claims c ON fl.Food_ID = c.Food_ID
GROUP BY fl.Meal_Type
ORDER BY Total_Claims DESC;


-- Query 13: Total quantity of food donated by each provider
SELECT 
    p.Name AS Provider_Name,
    p.Type AS Provider_Type,
    p.City,
    COUNT(fl.Food_ID) AS Total_Listings,
    SUM(fl.Quantity) AS Total_Quantity_Donated
FROM providers p
JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
GROUP BY p.Name, p.Type, p.City
ORDER BY Total_Quantity_Donated DESC
LIMIT 10;


-- Query 14: Food items expiring soon (next 30 days)
SELECT 
    fl.Food_Name,
    fl.Quantity,
    fl.Expiry_Date,
    fl.Location,
    p.Name AS Provider_Name,
    p.Contact
FROM food_listings fl
JOIN providers p ON fl.Provider_ID = p.Provider_ID
WHERE fl.Expiry_Date <= DATE('now', '+30 days')
AND fl.Expiry_Date >= DATE('now')
ORDER BY fl.Expiry_Date ASC
LIMIT 10;


-- Query 15: City wise claim success rate
SELECT 
    p.City,
    COUNT(c.Claim_ID) AS Total_Claims,
    SUM(CASE WHEN c.Status = 'Completed' THEN 1 ELSE 0 END) AS Completed,
    SUM(CASE WHEN c.Status = 'Cancelled' THEN 1 ELSE 0 END) AS Cancelled,
    SUM(CASE WHEN c.Status = 'Pending' THEN 1 ELSE 0 END) AS Pending,
    ROUND(SUM(CASE WHEN c.Status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / 
    COUNT(c.Claim_ID), 2) AS Success_Rate_Percent
FROM providers p
JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
JOIN claims c ON fl.Food_ID = c.Food_ID
GROUP BY p.City
ORDER BY Success_Rate_Percent DESC
LIMIT 10;


