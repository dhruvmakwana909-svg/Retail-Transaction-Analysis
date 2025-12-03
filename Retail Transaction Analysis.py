import pandas as pd 
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt 
import os
from datetime import datetime
from sklearn.ensemble import IsolationForest

df = pd.read_csv(r"C:\Users\DHRUV\Downloads\online_retail.csv\online_retail.csv", encoding='utf-8', low_memory=False)

OUT_DIR = 'output'
FIG_DIR = os.path.join(OUT_DIR, 'figures')
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


print("\n--- Data Info ---")
print(df.info())
print("\n--- First 5 Rows ---")
print(df.head(5))
print("\n--- Columns ---")
print(df.columns.tolist())

num_rows, num_cols = df.shape
print(f"\nRows: {num_rows}, Columns: {num_cols}")


num_summary = df.select_dtypes(include=[np.number]).describe().T
cat_summary = df.select_dtypes(include=['object', 'category']).nunique().sort_values()

num_summary.to_csv(os.path.join(OUT_DIR, 'numeric_summary.csv'))
cat_summary.to_frame('unique_count').to_csv(os.path.join(OUT_DIR, 'categorical_unique_counts.csv'))


for c in ['InvoiceNo', 'CustomerID', 'Country', 'Description']:
    if c in df.columns:
        print(f"\nUnique counts for {c}: {df[c].nunique()}")
        print(df[c].value_counts().head(10))


date_cols = [c for c in df.columns if 'Date' in c or 'date' in c or 'time' in c]
if date_cols:
    for dcol in date_cols:
        try:
            df[dcol] = pd.to_datetime(df[dcol], errors='coerce')
            print(f"Parsed {dcol} to datetime — nulls: {df[dcol].isna().sum()}")
        except Exception as e:
            print(f"Could not parse {dcol}: {e}")
else:
    print("No obvious date columns found. Rename if needed (e.g., to 'InvoiceDate').")


missing = df.isna().sum().sort_values(ascending=False)
missing_pct = (df.isna().mean() * 100).sort_values(ascending=False)
missing_df = pd.concat([missing, missing_pct], axis=1).rename(columns={0: 'missing_count', 1: 'missing_pct'})
missing_df.to_csv(os.path.join(OUT_DIR, 'missing_report.csv'))

#  Data Cleaning 
before = df.shape[0]
df.drop_duplicates(inplace=True)
after = df.shape[0]
print(f"Dropped {before - after} duplicate rows")

# Create Sales column
if 'UnitPrice' in df.columns and 'Quantity' in df.columns:
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Sales'] = df['UnitPrice'] * df['Quantity']
    print("Created Sales column")

# Fill missing CustomerID
if 'CustomerID' in df.columns:
    df['CustomerID'] = df['CustomerID'].fillna('Unknown')

# Handle returns
if 'InvoiceNo' in df.columns:
    df['IsReturn'] = df['InvoiceNo'].astype(str).str.startswith('C')

if 'Quantity' in df.columns:
    df['IsReturn'] = df.get('IsReturn', False) | (df['Quantity'] < 0)

# Drop rows with missing key fields
critical_cols = [c for c in ['InvoiceNo', 'UnitPrice', 'Quantity', 'Sales'] if c in df.columns]
df.dropna(subset=critical_cols, how='any', inplace=True)

# Outlier detection (optional)
if 'Sales' in df.columns:
    clf = IsolationForest(contamination=0.01, random_state=42)
    sales_vals = df[['Sales']].fillna(0).abs()
    try:
        df['OutlierScore'] = clf.fit_predict(sales_vals)
        df['IsOutlier'] = df['OutlierScore'] == -1
        print("Marked outliers in IsOutlier column")
    except Exception:
        df['IsOutlier'] = False

# Aggregations 
metrics = {}

if 'Country' in df.columns and 'Sales' in df.columns:
    country_sales = df.groupby('Country')['Sales'].sum().sort_values(ascending=False)
    country_sales.to_csv(os.path.join(OUT_DIR, 'country_sales.csv'))
    metrics['TopCountries'] = country_sales.head(10)

if 'CustomerID' in df.columns and 'Sales' in df.columns:
    top_customers = df.groupby('CustomerID')['Sales'].sum().sort_values(ascending=False)
    top_customers.to_csv(os.path.join(OUT_DIR, 'top_customers.csv'))
    metrics['TopCustomers'] = top_customers.head(20)

if date_cols and 'Sales' in df.columns:
    dcol = date_cols[0]
    df['OrderMonth'] = df[dcol].dt.to_period('M')
    monthly = df.groupby('OrderMonth')['Sales'].sum().sort_index()
    monthly.to_csv(os.path.join(OUT_DIR, 'monthly_sales.csv'))
    metrics['MonthlySales'] = monthly

# Visualizations 

#  Top 10 Countries by Sales
if 'TopCountries' in metrics:
    plt.figure(figsize=(10,5))
    metrics['TopCountries'].plot(kind='bar', color='skyblue')
    plt.title('Top 10 Countries by Sales')
    plt.ylabel('Sales')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'top10_country_sales.png'))
    plt.show()

#  Monthly Sales Trend
if 'MonthlySales' in metrics:
    plt.figure(figsize=(10,5))
    metrics['MonthlySales'].astype(float).plot(marker='o', color='green')
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Sales')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'monthly_sales_trend.png'))
    plt.show()

#  Quantity Distribution
if 'Quantity' in df.columns:
    plt.figure(figsize=(8,5))
    sns.histplot(df['Quantity'], bins=50, kde=True, color='orange')
    plt.title('Distribution of Quantity Sold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'quantity_distribution.png'))
    plt.show()

#  Correlation Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='Blues', fmt='.2f')
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'correlation_heatmap.png'))
plt.show()

#  Top 10 Products by Sales
if 'Description' in df.columns and 'Sales' in df.columns:
    top_products = df.groupby('Description')['Sales'].sum().nlargest(10)
    plt.figure(figsize=(10,6))
    top_products.plot(kind='barh', color='purple')
    plt.title('Top 10 Products by Sales')
    plt.xlabel('Sales')
    plt.ylabel('Product')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'top10_products.png'))
    plt.show()

# Save Outputs
clean_path = os.path.join(OUT_DIR, 'cleaned_online_retail.csv')
df.to_csv(clean_path, index=False)
print(f" Cleaned dataset saved to {clean_path}")
print(" EDA summary and figures saved to:", FIG_DIR)
