# Food Wastage Analytics Dashboard

An interactive data analytics dashboard built using Python, SQL, SQLite, and Streamlit to explore food donation and claim patterns, perform SQL-based analysis, and generate actionable insights through data visualization.

---

## Live Application

[Open Application](https://foodwastagemanagement-nxrsxyqlybvfv9dycnzaca.streamlit.app/)

---

## About The Project

Food wastage is a significant challenge — large amounts of surplus food are discarded daily while many individuals and organizations continue to face food insecurity. This project analyses food donation and claim data from a simulated food redistribution ecosystem to identify trends in provider participation, receiver activity, claim behaviour, and food availability across different cities.

By combining SQL analysis, data visualization, and an interactive dashboard, the project transforms raw data into meaningful insights that support a better understanding of food donation patterns and resource utilization.

---

## Business Problem

Food donation platforms generate large volumes of operational data. Without structured analysis, it becomes difficult to understand participation trends, claim success rates, provider performance, and food distribution patterns. This project addresses that challenge by analysing food donation data and presenting key findings through an interactive analytics dashboard — enabling faster, data-driven decision making.

---

## Dataset

The dataset used in this project is synthetically generated for educational and analytical purposes. It does not contain any real-world personal or organizational data.

| File | Records | Description |
|------|---------|-------------|
| providers_data.csv | 1,000 | Restaurants, supermarkets, grocery stores and catering services |
| receivers_data.csv | 1,000 | NGOs, charities, shelters and individuals |
| food_listings_data.csv | 1,000 | Food items with quantity, food type, meal type and expiry information |
| claims_data.csv | 1,000 | Food claims with Completed, Pending and Cancelled statuses |

---

## Objectives

- Analyse food donation and claim trends across cities
- Identify the most active providers and receivers on the platform
- Explore city-wise food distribution patterns
- Monitor food wastage indicators through data
- Enable interactive data exploration through dynamic filters
- Generate meaningful insights using SQL and data visualization

---

## Dashboard Features

### Insights and Trends
- 15 EDA charts covering provider activity, receiver behaviour, food type distribution, meal type analysis and claim patterns
- Every chart accompanied by a business insight

### Analysis
- 18 SQL business queries covering all key business questions
- Standard SQL with aggregate functions, joins and subqueries
- Advanced Common Table Expressions for provider performance scoring
- Window Functions for city-level ranking and running totals

### Filter and Search
- Dynamic filtering by city, food type, meal type and provider type
- Real-time results showing food listings, quantities and contact details

### Manage Listings
- Add new food listings
- View all existing records
- Update food listing details
- Delete outdated listings

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

| Category | Technology |
|----------|------------|
| Programming and Analysis | Python, Pandas, SQL |
| Database | SQLite |
| Data Visualization | Matplotlib |
| Dashboard Development | Streamlit |
| Version Control | Git and GitHub |

---

## Key Insights

- Barry Group emerged as the top provider with 5 successful claims and 179 units donated
- South Kathryn and New Carol recorded the highest number of food listings with 6 each
- Rice was the most frequently claimed food item with 45 claims
- 33.6% of claims were cancelled — nearly equal to the 33.9% completion rate, indicating a need for better follow-through mechanisms
- Vegan food contributed the highest overall donated quantity at 8,798 units
- Breakfast was both the most listed and most claimed meal category across all food types

---

## Skills Demonstrated

- Data Cleaning and Preparation
- Exploratory Data Analysis
- SQL Query Writing including CTEs and Window Functions
- Database Management with SQLite
- CRUD Operations
- Data Visualization with Matplotlib
- Dashboard Development with Streamlit
- Business Insight Generation
- Application Deployment on Streamlit Cloud

---

## How To Run

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/food_wastage_management.git
cd food_wastage_management
```

Install dependencies

```bash
pip install -r requirements.txt
```

Set up the database

```bash
python setup_db.py
```

Generate EDA charts

```bash
python eda.py
```

Launch the application

```bash
python -m streamlit run app/app.py
```

---

## Future Enhancements

- Real-time food donation tracking with live data integration
- Geographic visualization using interactive maps
- Automated reporting and scheduled insights
- Cloud database integration for scalability
- User authentication and role-based access control
- Predictive analytics for food demand forecasting
