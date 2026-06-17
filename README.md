# Local Food Wastage Management System

A data-driven platform that connects surplus food providers with those in need — 
built to reduce food wastage and improve food distribution efficiency.


## Problem Statement

Tons of surplus food is discarded daily by restaurants, supermarkets, and catering 
services while millions face food insecurity. This system bridges that gap by creating 
a centralized food redistribution platform where providers list surplus food, receivers 
claim it, and every transaction is tracked and analyzed.


## Live Demo

[Click here to view the app](https://foodwastagemanagement-nxrsxyqlybvfv9dycnzaca.streamlit.app/)


## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming |
| SQLite | Database storage |
| Pandas | Data manipulation |
| Matplotlib | EDA & visualizations |
| Streamlit | Interactive web dashboard |
| SQL | Data analysis & querying |


## Project Structure
food_wastage_management/

│

├── app/

│   ├── app.py          ← Main Streamlit application

│   └── startup.py      ← Auto database initialization

│

├── data/               ← Raw CSV datasets

├── database/           ← SQLite database (auto-generated)

├── assets/             ← EDA chart images

├── sql_queries/        ← All SQL queries documented

│

├── eda.py              ← EDA chart generation script

├── queries.py          ← SQL query execution script

├── setup_db.py         ← Database setup script

└── requirements.txt    ← Project dependencies


## Dataset Overview

| Dataset | Records | Description |
|---------|---------|-------------|
| Providers | 1,000 | Restaurants, Supermarkets, Grocery Stores, Catering Services |
| Receivers | 1,000 | NGOs, Charities, Shelters, Individuals |
| Food Listings | 1,000 | Available food items with quantity and expiry details |
| Claims | 1,000 | Food claims with status tracking |

---

## Key Features

- **Insights & Trends** — 15 EDA charts revealing donation patterns
- **Analysis** — 18 SQL queries including CTEs and Window Functions
- **Filter & Search** — Find food by city, type and meal preference
- **Manage Listings** — Full CRUD operations for food listings
- **Contact Details** — Direct provider and receiver contact info


## Key Findings

- **Barry Group** is the most reliable provider with 5 successful claims
- **Rice** is the most claimed food item with 45 claims
- **33.6%** of claims are cancelled — highlighting need for better follow-through
- **Vegan food** has the highest donated quantity (8,798 units)
- **Breakfast** is both the most listed and most claimed meal type


## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/food_wastage_management.git
cd food_wastage_management
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Generate EDA charts**
```bash
python eda.py
```

**4. Run the app**
```bash
python -m streamlit run app/app.py
```




