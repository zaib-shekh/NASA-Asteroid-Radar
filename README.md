# ☄️ NASA Asteroid Radar: End-to-End ELT Pipeline

A professional data engineering pipeline that ingests Near-Earth Object (NEO) data from NASA, stores it in a cloud data lake, and cleanses it using a distributed Spark environment.

## 🏗️ Architecture Overview
This project implements a decoupled **ELT (Extract, Load, Transform)** pattern:

1.  **Extraction (Local Python):** A script fetches raw JSON data from the NASA NeoWs API.
2.  **Bronze Layer (AWS S3):** The raw, immutable JSON data is landed in an S3 bucket for permanent storage.
3.  **Silver Layer (Databricks & PySpark):** Databricks Serverless compute is used to process the raw data. This includes flattening dynamic JSON arrays, enforcing a strict schema, and optimizing the storage format.
   ## 📂 Data Storage (Silver Layer)
After the PySpark transformation, the data is converted from raw JSON into an optimized **Apache Parquet** format and stored in the Silver Layer of our S3 bucket. This ensures the data is ready for high-performance analytics.

![S3 Silver Layer Screenshot](./s3_silver_layer.png)
*Figure 1: Verified Parquet output in AWS S3 silver_layer/ folder.*



## 🛠️ Technology Stack
* **Language:** Python 3.10+
* **Data Processing:** PySpark (Apache Spark), Pandas
* **Cloud Storage:** AWS S3 (Simple Storage Service)
* **Compute:** Databricks Serverless (Free Edition)
* **API:** NASA NeoWs (Near Earth Object Web Service)

## 🚀 Engineering Challenges & Solutions

### 1. Handling Dynamic JSON Keys
**Challenge:** The NASA API returns asteroids nested under specific date strings (e.g., `"2026-03-27": [...]`). PySpark's standard schema inference cannot handle these dynamic keys easily.
**Solution:** I implemented a Python pre-processing layer that flattens these nested structures into a standardized list of records before passing them to the Spark engine.

### 2. Bypassing Serverless FileSystem Locks
**Challenge:** Databricks Serverless environments often disable the Public DBFS and block traditional local file writes (`java.lang.SecurityException`).
**Solution:** I utilized the `boto3` library to bridge the gap between S3 and Spark. By fetching the data into memory and then creating a Spark DataFrame with an explicit schema, I bypassed the platform's storage restrictions.

### 3. Storage Optimization
**Challenge:** Raw JSON is slow to query and takes up significant space.
**Solution:** The final output is converted into **Apache Parquet**, a columnar storage format that provides high compression and faster read speeds for downstream analytics.

---

## ⚙️ Setup & Execution

### 1. Prerequisites
* **AWS Account:** An S3 Bucket (e.g., `orbital-bronze-abc-2026`).
* **NASA API Key:** Obtained from [api.nasa.gov](https://api.nasa.gov/).
* **Databricks:** A Community Edition or Serverless account.

### 2. Phase 1: Ingestion (Local)
1. Clone this repository.
2. Install dependencies: `pip install boto3 requests python-dotenv`
3. Add your credentials to your environment variables or a `.env` file.
4. Run the ingestion:
   ```bash
   python ingest_nasa_data.py
