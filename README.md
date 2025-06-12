# 📈 Stock Market Ticker Stream Cleanup

This project is focused on cleaning and processing stock market ticker stream data using **AWS Glue** and **PySpark**.  
The main objective is to filter, aggregate, and ensure data quality on stock ticker data stored on **Amazon S3**.

---

## 📂 Project Overview

The pipeline performs the following tasks:

- 📥 **Load Raw Data**: Reads stock ticker data from Amazon S3.
- 🔎 **Data Filtering**: Filters records where stock price is greater than zero.
- ➗ **Aggregation**: Computes average price from the filtered records.
- 💾 **Save Cleaned Data**: Writes the cleaned and processed data back to Amazon S3 in Parquet format with Snappy compression.

---

## 🛠 Technologies Used

- ☁️ AWS Glue
- 🗄️ AWS S3
- 🔥 PySpark
- 🐍 Python

---

## 📜 Script

The core logic is written in Python using AWS Glue APIs. The important steps are:

- 📚 **from_catalog()**: Reads data from AWS Glue Catalog.
- 🔍 **Filter**: Filters out invalid prices.
- ➕ **sparkAggregate()**: Performs aggregation (average price calculation).
- 💾 **write_dynamic_frame.from_options()**: Saves output to Amazon S3.

---
