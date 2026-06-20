# Food Wastage Analytics Dashboard

An interactive data analytics dashboard built using Python, SQL, SQLite, and Streamlit to explore food donation and claim patterns, perform SQL-based analysis, and generate actionable insights through data visualization and reporting.

---

## Live Application

[Open Application](https://foodwastagemanagement-nxrsxyqlybvfv9dycnzaca.streamlit.app/)

---

## About The Project

Food wastage is a significant challenge, with large amounts of surplus food being discarded while many individuals and organizations continue to face food insecurity. This project is based on a Local Food Wastage Management System where restaurants, supermarkets, grocery stores, and individuals can list surplus food, while NGOs and receivers can claim available donations.

The objective of this project is to analyze food donation and claim data to identify trends in food distribution, provider participation, receiver activity, claim behavior, and food availability across different cities. By combining SQL analysis, data visualization, and an interactive dashboard, the project transforms raw data into meaningful insights that support better understanding of food donation patterns and resource utilization.

---

## Business Problem

Food donation platforms generate large volumes of operational data, but without proper analysis it becomes difficult to understand participation trends, claim success rates, provider performance, and food distribution patterns. This project addresses that challenge by analyzing food donation data and presenting key findings through an interactive analytics dashboard.

---

## Dataset

This project uses a synthetically generated dataset provided as part of an internship project. The dataset was created for educational and analytical purposes and does not contain real-world personal or organizational data.

The dataset consists of four structured CSV files:

| File                   | Records | Description                                                           |
| ---------------------- | ------- | --------------------------------------------------------------------- |
| providers_data.csv     | 1,000   | Restaurants, supermarkets, grocery stores and catering services       |
| receivers_data.csv     | 1,000   | NGOs, charities, shelters and individuals                             |
| food_listings_data.csv | 1,000   | Food items with quantity, food type, meal type and expiry information |
| claims_data.csv        | 1,000   | Food claims with Completed, Pending and Cancelled statuses            |

---

## Objectives

* Analyze food donation and claim trends
* Identify active providers and receivers
* Explore city-wise food distribution patterns
* Monitor food wastage indicators
* Enable interactive data exploration through filters
* Generate meaningful insights using SQL and data visualization

---

## Dashboard Features

### Data Analysis

* 15 EDA charts exploring donation and claim patterns
* Provider and receiver activity analysis
* Food type and meal type analysis
* Claim status distribution analysis
* City-wise food distribution insights

### SQL Analytics

* 18 SQL business queries
* Aggregate Functions
* Joins and Subqueries
* Common Table Expressions (CTEs)
* Window Functions

### Interactive Dashboard

* Dynamic filtering by city
* Food type filtering
* Meal type filtering
* Search functionality
* Interactive charts and visualizations

### Database Operations

* Create food listings
* Read existing records
* Update food listing details
* Delete food listings
* View provider and receiver information

---

## Project Structure

food_wastage_management/

│

├── app/

│   ├── app.py

│   └── startup.py

│

├── data/

│   ├── providers_data.csv

│   ├── receivers_data.csv

│   ├── food_listings_data.csv

│   └── claims_data.csv

│

├── database/

│   └── food_wastage.db

│

├── assets/

├── sql_queries/

│   └── queries.sql

│

├── eda.py

├── queries.py

├── setup_db.py

├── requirements.txt

└── README.md

---

## Tech Stack

### Programming & Analysis

* Python
* Pandas
* SQL

### Database

* SQLite

### Data Visualization

* Matplotlib

### Dashboard Development

* Streamlit

---

## Key Insights

* Barry Group emerged as the top provider with 5 successful claims and 179 units donated.
* South Kathryn and New Carol recorded the highest number of food listings.
* Rice was the most frequently claimed food item.
* Approximately 33.6% of claims were cancelled, nearly matching the completion rate.
* Vegan food contributed the highest overall donated quantity.
* Breakfast was both the most listed and most claimed meal category.

---

## Skills Demonstrated

* Data Cleaning and Preparation
* Exploratory Data Analysis (EDA)
* SQL Query Writing
* Database Management
* CRUD Operations
* Data Visualization
* Dashboard Development
* Business Insight Generation
* Interactive Reporting

---

## How To Run

```bash
git clone https://github.com/YOUR_USERNAME/food_wastage_management.git

cd food_wastage_management

pip install -r requirements.txt

python setup_db.py

python eda.py

streamlit run app/app.py
```

---

## Future Enhancements

* Real-time food donation tracking
* Advanced dashboard analytics
* Geographic visualization using maps
* Automated reporting
* Cloud database integration
* User authentication and access control


