# EXPLORATORY DATA ANALYSIS : 

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import warnings
warnings.filterwarnings('ignore')

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DB_PATH    = os.path.join(BASE_DIR, "database", "food_wastage.db")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
providers     = pd.read_sql("SELECT * FROM providers",     conn)
receivers     = pd.read_sql("SELECT * FROM receivers",     conn)
food_listings = pd.read_sql("SELECT * FROM food_listings", conn)
claims        = pd.read_sql("SELECT * FROM claims",        conn)

# ── Dark Theme Settings ────────────────────────────────────────────────────────
BG      = '#0d1117'
AX_BG   = '#161b22'
TEXT    = '#e6edf3'
GRID    = '#21262d'
COLORS  = ['#2ecc71','#27ae60','#1abc9c','#16a085','#f39c12',
           '#e67e22','#e74c3c','#9b59b6','#3498db','#2980b9']

def apply_dark(fig, ax_list):
    fig.patch.set_facecolor(BG)
    for ax in (ax_list if isinstance(ax_list, list) else [ax_list]):
        ax.set_facecolor(AX_BG)
        ax.tick_params(colors=TEXT, labelsize=9)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_edgecolor(GRID)
        ax.yaxis.grid(True, color=GRID, linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)

def save_chart(filename):
    path = os.path.join(ASSETS_DIR, filename)
    plt.savefig(path, bbox_inches='tight', dpi=130,
                facecolor=BG, edgecolor='none')
    plt.close()
    print(f" Saved: {filename}")

print("Generating dark-themed charts...\n")

# Chart 1 — Provider Type Distribution
provider_type = providers['Type'].value_counts()
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(provider_type.index, provider_type.values, color=COLORS, width=0.5)
ax.set_title('Provider Type Distribution', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Provider Type', labelpad=8)
ax.set_ylabel('Count', labelpad=8)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2,
            str(int(bar.get_height())), ha='center', va='bottom',
            color=TEXT, fontsize=9, fontweight='600')
plt.xticks(rotation=10)
apply_dark(fig, ax)
save_chart('chart1_provider_type.png')

# Chart 2 — Receiver Type Distribution
receiver_type = receivers['Type'].value_counts()
fig, ax = plt.subplots(figsize=(6, 5))
wedges, texts, autotexts = ax.pie(
    receiver_type.values, labels=receiver_type.index,
    autopct='%1.1f%%', colors=COLORS, startangle=140,
    wedgeprops={'edgecolor': BG, 'linewidth': 2})
for t in texts:     t.set_color(TEXT); t.set_fontsize(10)
for a in autotexts: a.set_color(BG);   a.set_fontsize(9); a.set_fontweight('bold')
ax.set_title('Receiver Type Distribution', fontsize=13, fontweight='bold', pad=12, color=TEXT)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
save_chart('chart2_receiver_type.png')

# Chart 3 — Food Type Distribution
food_type = food_listings['Food_Type'].value_counts()
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(food_type.index, food_type.values, color=COLORS[:3], width=0.45)
ax.set_title('Food Type Distribution', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Food Type', labelpad=8)
ax.set_ylabel('Count', labelpad=8)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
            str(int(bar.get_height())), ha='center', va='bottom',
            color=TEXT, fontsize=9, fontweight='600')
apply_dark(fig, ax)
save_chart('chart3_food_type.png')

# Chart 4 — Meal Type Distribution
meal_type = food_listings['Meal_Type'].value_counts()
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(meal_type.index, meal_type.values, color=COLORS[:4], height=0.5)
ax.set_title('Meal Type Distribution', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Count', labelpad=8)
for bar in bars:
    ax.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
            str(int(bar.get_width())), va='center',
            color=TEXT, fontsize=9, fontweight='600')
apply_dark(fig, ax)
save_chart('chart4_meal_type.png')

# Chart 5 — Top 10 Cities by Food Listings
city_listings = food_listings['Location'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.bar(city_listings.index, city_listings.values, color=COLORS, width=0.6)
ax.set_title('Top 10 Cities by Food Listings', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('City', labelpad=8)
ax.set_ylabel('Number of Listings', labelpad=8)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
            str(int(bar.get_height())), ha='center', va='bottom',
            color=TEXT, fontsize=8, fontweight='600')
plt.xticks(rotation=25, ha='right')
apply_dark(fig, ax)
save_chart('chart5_city_listings.png')

# Chart 6 — Provider Type vs Quantity
prov_qty = food_listings.groupby('Provider_Type')['Quantity'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(prov_qty.index, prov_qty.values, color=COLORS, width=0.5)
ax.set_title('Provider Type vs Total Quantity', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Provider Type', labelpad=8)
ax.set_ylabel('Total Quantity', labelpad=8)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
            f"{int(bar.get_height()):,}", ha='center', va='bottom',
            color=TEXT, fontsize=8, fontweight='600')
plt.xticks(rotation=10)
apply_dark(fig, ax)
save_chart('chart6_provider_quantity.png')

# Chart 7 — Food Type vs Quantity
food_qty = food_listings.groupby('Food_Type')['Quantity'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(food_qty.index, food_qty.values, color=COLORS[:3], width=0.45)
ax.set_title('Food Type vs Total Quantity', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Food Type', labelpad=8)
ax.set_ylabel('Total Quantity', labelpad=8)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
            f"{int(bar.get_height()):,}", ha='center', va='bottom',
            color=TEXT, fontsize=9, fontweight='600')
apply_dark(fig, ax)
save_chart('chart7_foodtype_quantity.png')

# Chart 8 — Meal Type vs Quantity
meal_qty = food_listings.groupby('Meal_Type')['Quantity'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(meal_qty.index, meal_qty.values, color=COLORS[:4], width=0.5)
ax.set_title('Meal Type vs Total Quantity', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Meal Type', labelpad=8)
ax.set_ylabel('Total Quantity', labelpad=8)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
            f"{int(bar.get_height()):,}", ha='center', va='bottom',
            color=TEXT, fontsize=9, fontweight='600')
apply_dark(fig, ax)
save_chart('chart8_mealtype_quantity.png')

# Chart 9 — City + Provider Type + Quantity
top5 = food_listings['Location'].value_counts().head(5).index
filt = food_listings[food_listings['Location'].isin(top5)]
pivot = filt.pivot_table(values='Quantity', index='Location',
                         columns='Provider_Type', aggfunc='sum', fill_value=0)
fig, ax = plt.subplots(figsize=(10, 5))
pivot.plot(kind='bar', ax=ax, color=COLORS[:len(pivot.columns)], width=0.65)
ax.set_title('City + Provider Type + Quantity (Top 5)', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('City', labelpad=8)
ax.set_ylabel('Total Quantity', labelpad=8)
plt.xticks(rotation=12)
ax.legend(title='Provider Type', facecolor=AX_BG, edgecolor=GRID,
          labelcolor=TEXT, title_fontsize=8, fontsize=8)
apply_dark(fig, ax)
save_chart('chart9_city_provider_quantity.png')

# Chart 10 — Food Type + Meal Type + Quantity
pivot2 = food_listings.pivot_table(values='Quantity', index='Food_Type',
                                   columns='Meal_Type', aggfunc='sum', fill_value=0)
fig, ax = plt.subplots(figsize=(9, 5))
pivot2.plot(kind='bar', ax=ax, color=COLORS[:len(pivot2.columns)], width=0.65)
ax.set_title('Food Type + Meal Type + Quantity', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Food Type', labelpad=8)
ax.set_ylabel('Total Quantity', labelpad=8)
plt.xticks(rotation=0)
ax.legend(title='Meal Type', facecolor=AX_BG, edgecolor=GRID,
          labelcolor=TEXT, title_fontsize=8, fontsize=8)
apply_dark(fig, ax)
save_chart('chart10_foodtype_mealtype_quantity.png')

# Chart 11 — Top 10 Providers by Claims
pc = pd.read_sql("""
    SELECT p.Name, COUNT(c.Claim_ID) AS Total_Claims
    FROM providers p
    JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
    JOIN claims c ON fl.Food_ID = c.Food_ID
    GROUP BY p.Name ORDER BY Total_Claims DESC LIMIT 10
""", conn)
fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.bar(pc['Name'], pc['Total_Claims'], color=COLORS, width=0.6)
ax.set_title('Top 10 Providers by Number of Claims', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Provider', labelpad=8)
ax.set_ylabel('Total Claims', labelpad=8)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
            str(int(bar.get_height())), ha='center', va='bottom',
            color=TEXT, fontsize=8, fontweight='600')
plt.xticks(rotation=28, ha='right')
apply_dark(fig, ax)
save_chart('chart11_provider_claims.png')

# Chart 12 — Top 10 Receivers by Claims
rc = pd.read_sql("""
    SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims
    FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID
    GROUP BY r.Name ORDER BY Total_Claims DESC LIMIT 10
""", conn)
fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.bar(rc['Name'], rc['Total_Claims'], color=COLORS, width=0.6)
ax.set_title('Top 10 Receivers by Number of Claims', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Receiver', labelpad=8)
ax.set_ylabel('Total Claims', labelpad=8)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
            str(int(bar.get_height())), ha='center', va='bottom',
            color=TEXT, fontsize=8, fontweight='600')
plt.xticks(rotation=28, ha='right')
apply_dark(fig, ax)
save_chart('chart12_receiver_claims.png')

# Chart 13 — Claim Status Distribution
claim_status = claims['Status'].value_counts()
fig, ax = plt.subplots(figsize=(6, 5))
wedges, texts, autotexts = ax.pie(
    claim_status.values, labels=claim_status.index,
    autopct='%1.1f%%',
    colors=['#2ecc71','#e74c3c','#f39c12'],
    startangle=140,
    wedgeprops={'edgecolor': BG, 'linewidth': 2})
for t in texts:     t.set_color(TEXT); t.set_fontsize(10)
for a in autotexts: a.set_color(BG);   a.set_fontsize(9); a.set_fontweight('bold')
ax.set_title('Claim Status Distribution', fontsize=13, fontweight='bold', pad=12, color=TEXT)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
save_chart('chart13_claim_status.png')

# Chart 14 — Top Receivers by Completed Claims
tr = pd.read_sql("""
    SELECT r.Name, COUNT(c.Claim_ID) AS Completed_Claims
    FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID
    WHERE c.Status='Completed' GROUP BY r.Name
    ORDER BY Completed_Claims DESC LIMIT 10
""", conn)
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(tr['Name'], tr['Completed_Claims'], color=COLORS, height=0.55)
ax.set_title('Top 10 Receivers by Completed Claims', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Completed Claims', labelpad=8)
for bar in bars:
    ax.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2,
            str(int(bar.get_width())), va='center',
            color=TEXT, fontsize=8, fontweight='600')
apply_dark(fig, ax)
save_chart('chart14_top_receivers.png')

# Chart 15 — Top Providers by Successful Claims
tp = pd.read_sql("""
    SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
    FROM providers p
    JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
    JOIN claims c ON fl.Food_ID = c.Food_ID
    WHERE c.Status='Completed' GROUP BY p.Name
    ORDER BY Successful_Claims DESC LIMIT 10
""", conn)
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(tp['Name'], tp['Successful_Claims'], color=COLORS, height=0.55)
ax.set_title('Top 10 Providers by Successful Claims', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Successful Claims', labelpad=8)
for bar in bars:
    ax.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2,
            str(int(bar.get_width())), va='center',
            color=TEXT, fontsize=8, fontweight='600')
apply_dark(fig, ax)
save_chart('chart15_top_providers.png')

conn.close()
print("\n All charts saved!")