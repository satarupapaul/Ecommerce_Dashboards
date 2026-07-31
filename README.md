# 👗 Fashion E-Commerce Analytics Dashboard

An interactive multi-page **E-Commerce Analytics Dashboard** built with **Python, Streamlit, Pandas, NumPy, Plotly, and MySQL**. 

This application provides real-time sales insights, product performance analytics, dataset exploration, statistical breakdowns, and user authentication with seamless offline CSV fallback.

---

## 🌟 Key Features

- **🔐 User Authentication & Demo Mode:**
  - Login and Sign-Up authentication powered by MySQL.
  - **Quick Demo Mode** to explore the dashboard instantly without needing MySQL database setup.

- **📊 Comprehensive Sales Analytics:**
  - Track Total Revenue, Total Products Sold, Average Sale Amount, and Maximum Sale Value.
  - Category-wise revenue breakdown using interactive Plotly pie charts.
  - City-wise and Brand-wise performance visual analytics.

- **🛍️ Product Performance Analytics:**
  - Top 10 revenue-generating products & bottom 5 product identification.
  - Product quantity distribution and ranking summaries.
  - Automated Pandas and NumPy metrics (Mean, Median, Standard Deviation, Max/Min).

- **📂 Dataset Viewer & Processing Pipeline:**
  - Interactive table filtering and dataset inspection.
  - Missing value and duplicate record diagnostic summaries.
  - Export processed dataset to CSV with one click.

- **⚡ Dual Data Storage Engine:**
  - Connects to **MySQL Database** when available.
  - Graceful automatic **CSV Fallback** when MySQL is offline.

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Language** | Python 3.9+ |
| **Web Framework** | Streamlit |
| **Data Analysis** | Pandas, NumPy |
| **Data Visualization** | Plotly Express |
| **Database** | MySQL (with mysql-connector-python) |

---

## 📂 Project Structure

```text
fashion_ecommerce_dashboard/
├── app.py                  # Main Streamlit application entry point
├── database.py             # MySQL connection & user auth helper functions
├── analysis.py             # Standalone Python script for SQL-based Pandas/NumPy analysis
├── csv_analysis.py         # Standalone Python script for CSV analysis
├── generate_dataset.py     # Script to generate synthetic 500-record e-commerce sales dataset
├── import_csv_to_mysql.py  # Script to import generated CSV into MySQL database
├── data/
│   └── fashion_sales.csv   # Primary CSV sales dataset
├── pages/
│   ├── dashboard.py        # Main sales dashboard component
│   ├── sales_analytics.py  # Detailed sales analytics component
│   ├── product_analytics.py# Product performance analytics component
│   └── dataset_viewer.py   # Dataset processing & viewer component
├── .gitignore              # Ignored files (cache, env, etc.)
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have **Python 3.9+** installed on your system.

### 2. Clone the Repository

```bash
git clone https://github.com/satarupapaul/Ecommerce_Dashboards.git
cd Ecommerce_Dashboards
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard

Launch the application directly using Streamlit:

```bash
streamlit run app.py
```

> **Note:** If MySQL is not running on your machine, select **Demo Access** on the login page to immediately start exploring all analytics features in offline mode.

---

## 🗄️ (Optional) MySQL Setup Guide

If you wish to run the app with a live MySQL database backend:

1. Open MySQL workbench or shell and create the database:
   ```sql
   CREATE DATABASE fashion_ecommerce;
   ```
2. Create the `users` table:
   ```sql
   USE fashion_ecommerce;

   CREATE TABLE users (
       user_id INT AUTO_INCREMENT PRIMARY KEY,
       full_name VARCHAR(100) NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL
   );
   ```
3. Update database credentials in `database.py` if necessary (`host`, `user`, `password`).
4. Import the dataset into MySQL:
   ```bash
   python import_csv_to_mysql.py
   ```

---

## 📈 Data Pipeline Workflow

```text
Synthetic Dataset Generator (generate_dataset.py)
                      ↓
           data/fashion_sales.csv
                      ↓
     Import to MySQL (import_csv_to_mysql.py)
                      ↓
      Streamlit Web Dashboard (app.py)
  (Pandas Data Cleaning + NumPy Metrics + Plotly Visuals)
```

---

## 📝 License

Distributed under the MIT License. Feel free to use and adapt this project for your portfolio or learning.
