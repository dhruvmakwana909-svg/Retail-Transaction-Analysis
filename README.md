Online Retail Data Cleaning & EDA Pipeline

A fully automated Python pipeline for cleaning, processing, and analyzing the Online Retail dataset, generating business insights, anomaly detection, and publication-ready visualizations.

Project Overview

This project builds a complete end-to-end workflow for Online Retail data:
Cleans messy raw data
Identifies returns & missing values
Detects anomalies using Isolation Forest
Builds business KPIs (countries, customers, products)
Performs time-series analysis
Generates professional-level plots
Saves clean data + all reports automatically

 Project Structure
├── online_retail_analysis.py       # Main Python script  

├── output/

│   ├── cleaned_online_retail.csv   # Clean final dataset

│   ├── numeric_summary.csv

│   ├── categorical_unique_counts.csv

│   ├── missing_report.csv

│   ├── top_customers.csv

│   ├── country_sales.csv

│   ├── monthly_sales.csv

│   └── figures/

│       ├── top10_country_sales.png

│       ├── monthly_sales_trend.png

│       ├── quantity_distribution.png

│       ├── correlation_heatmap.png

│       └── top10_products.png

└── README.md

 Key Features
 
1. Data Understanding
   
Displays dataset info, sample rows, and column summary
Generates:
Numeric feature summary
Unique counts for categorical columns
Missing value report (CSV)

3. Data Cleaning
   
Removes duplicate rows
Converts numeric fields
Creates a Sales column
Fills missing CustomerID
Detects return orders using:
Negative quantity
Invoice starting with “C”
Drops rows with missing critical fields
Parses date columns automatically

4. Anomaly Detection
   
Uses Isolation Forest to detect unusually high/low Sales values.
Adds:
OutlierScore
IsOutlier flag

4. Business-Level Analytics

Top Countries by Sales
Top Customers by Sales
Top 10 Products
Monthly Sales Trend
All CSV outputs saved in the output/ folder.

5. Visualizations

Automatically generates:

Visualization	Description
Top 10 Countries	Bar chart
Monthly Sales Trend	Time-series line plot
Quantity Distribution	Histogram + KDE
Correlation Heatmap	Numeric correlations
Top Products	Horizontal bar chart

All images saved under output/figures/.

Technologies Used
Python 3.x
Pandas
NumPy
Matplotlib
Seaborn
Sklearn (IsolationForest)
OS / Datetime

Outputs (Automatically Generated)
 Cleaned dataset
 Summaries (numeric, categorical, missing)
 Business reports (country, customer, product, monthly)
 Visualizations
 Outlier flags


<img width="1000" height="500" alt="Figure_1" src="https://github.com/user-attachments/assets/670a495a-32e1-4692-bb43-c719620fddb8" />

<img width="1000" height="500" alt="Figure_2" src="https://github.com/user-attachments/assets/0efa28b2-488c-4bda-bec9-c69392226c4d" />

<img width="800" height="500" alt="Figure_3" src="https://github.com/user-attachments/assets/b4fef277-8d54-4cc5-bc97-0d3c00251fe2" />

<img width="800" height="600" alt="Figure_4" src="https://github.com/user-attachments/assets/1beca7bf-d0e8-42dc-89b9-5a99e83141fb" />

<img width="1000" height="600" alt="Figure_5" src="https://github.com/user-attachments/assets/16561684-ff6f-4b4b-9f47-e6f6dbd48635" />
