"""
queries.py
----------
All SQL queries for the Local Food Wastage Management System.
Command: python queries.py
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect('database/food_wastage.db')

queries = {
    "Q1: Providers per City": """
        SELECT City, COUNT(*) AS Total_Providers
        FROM providers
        GROUP BY City
        ORDER BY Total_Providers DESC
        LIMIT 5
    """,

    "Q2: Provider Type Contributions": """
        SELECT Provider_Type,
               COUNT(*) AS Total_Listings,
               SUM(Quantity) AS Total_Quantity
        FROM food_listings
        GROUP BY Provider_Type
        ORDER BY Total_Quantity DESC
    """,

    "Q3: Providers in Specific City": """
        SELECT Name, Type, Address, Contact
        FROM providers
        WHERE City = 'New Carol'
    """,

    "Q4: Receivers with Most Claims": """
        SELECT r.Name, r.Type, COUNT(c.Claim_ID) AS Total_Claims
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.Name, r.Type
        ORDER BY Total_Claims DESC
        LIMIT 5
    """,

    "Q5: Total Food Available": """
        SELECT SUM(Quantity) AS Total_Food_Available,
               COUNT(*) AS Total_Listings,
               ROUND(AVG(Quantity), 2) AS Avg_Quantity_Per_Listing
        FROM food_listings
    """,

    "Q6: City with Most Listings": """
        SELECT Location AS City,
               COUNT(*) AS Total_Listings,
               SUM(Quantity) AS Total_Quantity
        FROM food_listings
        GROUP BY Location
        ORDER BY Total_Listings DESC
        LIMIT 5
    """,

    "Q7: Most Common Food Types": """
        SELECT Food_Type,
               COUNT(*) AS Total_Listings,
               SUM(Quantity) AS Total_Quantity,
               ROUND(AVG(Quantity), 2) AS Avg_Quantity
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Total_Listings DESC
    """,

    "Q8: Claims per Food Item": """
        SELECT fl.Food_Name, fl.Food_Type,
               COUNT(c.Claim_ID) AS Total_Claims
        FROM food_listings fl
        LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
        GROUP BY fl.Food_Name, fl.Food_Type
        ORDER BY Total_Claims DESC
        LIMIT 5
    """,

    "Q9: Provider with Most Successful Claims": """
        SELECT p.Name, p.Type, p.City,
               COUNT(c.Claim_ID) AS Successful_Claims
        FROM providers p
        JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
        JOIN claims c ON fl.Food_ID = c.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Name, p.Type, p.City
        ORDER BY Successful_Claims DESC
        LIMIT 5
    """,

    "Q10: Claim Status Percentage": """
        SELECT Status,
               COUNT(*) AS Total_Claims,
               ROUND(COUNT(*) * 100.0 /
               (SELECT COUNT(*) FROM claims), 2) AS Percentage
        FROM claims
        GROUP BY Status
        ORDER BY Percentage DESC
    """,

    "Q11: Avg Quantity per Receiver": """
        SELECT r.Name, r.Type,
               COUNT(c.Claim_ID) AS Total_Claims,
               ROUND(AVG(fl.Quantity), 2) AS Avg_Quantity
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        JOIN food_listings fl ON c.Food_ID = fl.Food_ID
        GROUP BY r.Name, r.Type
        ORDER BY Avg_Quantity DESC
        LIMIT 5
    """,

    "Q12: Most Claimed Meal Type": """
        SELECT fl.Meal_Type,
               COUNT(c.Claim_ID) AS Total_Claims,
               SUM(fl.Quantity) AS Total_Quantity
        FROM food_listings fl
        JOIN claims c ON fl.Food_ID = c.Food_ID
        GROUP BY fl.Meal_Type
        ORDER BY Total_Claims DESC
    """,

    "Q13: Total Quantity Donated by Provider": """
        SELECT p.Name, p.Type, p.City,
               SUM(fl.Quantity) AS Total_Quantity_Donated
        FROM providers p
        JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
        GROUP BY p.Name, p.Type, p.City
        ORDER BY Total_Quantity_Donated DESC
        LIMIT 5
    """,

    "Q14: Food Items Expiring Soon": """
        SELECT fl.Food_Name, fl.Quantity,
               fl.Expiry_Date, fl.Location,
               p.Name AS Provider_Name, p.Contact
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        ORDER BY fl.Expiry_Date ASC
        LIMIT 5
    """,

    "Q15: City Wise Claim Success Rate": """
        SELECT p.City,
               COUNT(c.Claim_ID) AS Total_Claims,
               SUM(CASE WHEN c.Status='Completed' THEN 1 ELSE 0 END) AS Completed,
               SUM(CASE WHEN c.Status='Cancelled' THEN 1 ELSE 0 END) AS Cancelled,
               ROUND(SUM(CASE WHEN c.Status='Completed' THEN 1 ELSE 0 END) * 100.0 /
               COUNT(c.Claim_ID), 2) AS Success_Rate
        FROM providers p
        JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
        JOIN claims c ON fl.Food_ID = c.Food_ID
        GROUP BY p.City
        ORDER BY Success_Rate DESC
        LIMIT 5
    """,

    "Q16: CTE - Provider Performance Analysis": """
        WITH provider_stats AS (
            SELECT
                fl.Provider_ID,
                COUNT(DISTINCT fl.Food_ID) AS Total_Listings,
                SUM(fl.Quantity) AS Total_Quantity,
                COUNT(c.Claim_ID) AS Total_Claims
            FROM food_listings fl
            LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
            GROUP BY fl.Provider_ID
        ),
        completed_stats AS (
            SELECT
                fl.Provider_ID,
                COUNT(c.Claim_ID) AS Completed_Claims
            FROM food_listings fl
            LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
            WHERE c.Status = 'Completed'
            GROUP BY fl.Provider_ID
        )
        SELECT
            p.Name AS Provider_Name,
            p.Type AS Provider_Type,
            p.City,
            ps.Total_Listings,
            ps.Total_Quantity,
            ps.Total_Claims,
            COALESCE(cs.Completed_Claims, 0) AS Completed_Claims,
            ROUND(COALESCE(cs.Completed_Claims, 0) * 100.0 /
            ps.Total_Claims, 2) AS Success_Rate
        FROM providers p
        JOIN provider_stats ps ON p.Provider_ID = ps.Provider_ID
        LEFT JOIN completed_stats cs ON p.Provider_ID = cs.Provider_ID
        WHERE ps.Total_Claims > 0
        ORDER BY Success_Rate DESC
        LIMIT 10
    """,

    "Q17: Window Function - Food Quantity Rank by City": """
        SELECT
            Food_Name,
            Location AS City,
            Food_Type,
            Quantity,
            RANK() OVER (
                PARTITION BY Location
                ORDER BY Quantity DESC
            ) AS Rank_In_City,
            SUM(Quantity) OVER (
                PARTITION BY Location
            ) AS City_Total_Quantity,
            ROUND(Quantity * 100.0 / SUM(Quantity) OVER (
                PARTITION BY Location
            ), 2) AS Pct_Of_City_Total
        FROM food_listings
        ORDER BY City, Rank_In_City
        LIMIT 15
    """,

    "Q18: Window Function - Running Total of Claims by Date": """
        SELECT
            DATE(Timestamp) AS Claim_Date,
            COUNT(*) AS Daily_Claims,
            SUM(COUNT(*)) OVER (
                ORDER BY DATE(Timestamp)
            ) AS Running_Total,
            ROUND(AVG(COUNT(*)) OVER (
                ORDER BY DATE(Timestamp)
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ), 2) AS Moving_Avg_3Day
        FROM claims
        GROUP BY DATE(Timestamp)
        ORDER BY Claim_Date
        LIMIT 15
    """
}

#  for displaying results : 
for title, query in queries.items():
    print(f"\n{'='*55}")
    print(f"{title}")
    print('='*55)
    df = pd.read_sql(query, conn)
    print(df.to_string(index=False))

conn.close()
print("\n ANALYSIS DONE !")