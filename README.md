# E-Commerce Big Data Analytics

## Project Overview

This project analyzes an online retail dataset using Apache PySpark to demonstrate a complete Big Data analytics workflow.

The project covers data loading, data cleaning, feature engineering, sales analysis, customer analysis, RFM segmentation, and interactive dashboard visualization.

The final results are presented through an interactive Streamlit dashboard.

---

## Project Objectives

The main objectives of this project are:

* Process a large retail transaction dataset using PySpark.
* Clean and prepare raw transactional data.
* Create useful analytical features.
* Analyze sales and revenue trends.
* Identify high-performing products and countries.
* Analyze customer purchasing behavior.
* Segment customers using RFM analysis.
* Build an interactive business dashboard.

---

## Dataset

The project uses the Online Retail dataset.

The dataset contains transactional information such as:

* Invoice Number
* Stock Code
* Product Description
* Quantity
* Invoice Date
* Unit Price
* Customer ID
* Country

---

## Technologies Used

### Data Processing

* Python
* Apache PySpark

### Data Analysis

* PySpark SQL
* Pandas

### Visualization

* Plotly

### Dashboard

* Streamlit

### Development Environment

* Visual Studio Code
* Jupyter Notebook

---

## Data Processing Pipeline

The project follows this workflow:

```text
Raw CSV Data
      ↓
Data Loading
      ↓
Data Cleaning
      ↓
Feature Engineering
      ↓
Exploratory Analysis
      ↓
Customer Analysis
      ↓
RFM Segmentation
      ↓
Processed CSV Data
      ↓
Streamlit Dashboard
```

---

## Data Cleaning

The cleaning stage includes:

* Handling missing Customer IDs.
* Removing invalid quantities.
* Removing invalid unit prices.
* Removing duplicate records.
* Creating the TotalPrice column.
* Converting InvoiceDate into a proper timestamp.
* Handling multiple possible date formats.

The TotalPrice feature is calculated as:

```text
TotalPrice = Quantity × UnitPrice
```

---

## Feature Engineering

Additional features were created from the transaction date:

* Year
* Month
* Day
* Hour
* YearMonth
* TotalPrice

These features allow the analysis of sales patterns over time.

---

## Sales Analysis

The project analyzes:

* Total revenue.
* Number of orders.
* Revenue by month.
* Revenue by country.
* Top-performing products.
* Revenue by hour.
* Average order value.

These metrics help identify important sales trends and business performance.

---

## Customer Analysis

Customer behavior is analyzed using:

* Number of unique customers.
* Customer revenue.
* Number of orders per customer.
* Average customer purchasing activity.
* Top customers by revenue.

---

## RFM Analysis

RFM analysis is used to segment customers based on three dimensions:

### Recency

How recently a customer made a purchase.

### Frequency

How frequently a customer makes purchases.

### Monetary

How much money a customer has spent.

The three metrics are combined to create customer segments that help identify valuable and less-active customers.

---

## Interactive Dashboard

The Streamlit dashboard contains three main sections:

### Overview

Provides a high-level summary of:

* Revenue
* Orders
* Customers
* Products
* Monthly revenue trends
* Top countries
* Top products

### Sales Analysis

Provides detailed analysis of:

* Monthly revenue
* Country performance
* Product performance
* Revenue by hour

### Customer Analysis

Provides:

* Top customers
* Customer revenue
* Customer details
* RFM segmentation
* RFM customer information

The dashboard also includes interactive filters for analyzing different parts of the dataset.

---

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit dashboard

From the project root:

```bash
python -m streamlit run dashboard/dashboard.py
```

The dashboard will then open in the browser.

---

## Project Structure

```text
Big_Data_Ecommerce/
│
├── Data/
│   └── OnlineRetail.csv
│
├── notebook/
│   └── analysis.ipynb
│
├── dashboard/
│   ├── dashboard.py
│   ├── data_clean.csv
│   └── rfm_customers.csv
│
├── README.md
└── requirements.txt
```

---

## Conclusion

This project demonstrates how PySpark can be used to process and analyze transactional retail data and transform raw data into meaningful business insights.

The final Streamlit dashboard provides an interactive interface for exploring sales performance and customer behavior.

The project combines Big Data processing, data analytics, customer segmentation, and business intelligence in one end-to-end solution.
