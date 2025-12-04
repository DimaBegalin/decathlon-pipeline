# Data Pipeline Project — Website to Database (SIS2)

**Course:** Data Collection & Preparation  
**Format:** Team Project (2 students)  
**Submission deadline:** December 4, 2025

---

## Project Description

This project implements a complete automated data pipeline from a dynamic website to a database.

The system performs the following steps:

- Scrapes data from a JavaScript-rendered website using Selenium  
- Cleans and preprocesses the dataset  
- Stores processed data into a SQLite database  
- Automates the full workflow using Apache Airflow  

The goal of this project is to demonstrate understanding of:

- Web scraping from dynamic websites  
- Data cleaning and transformation  
- Database design and insertion  
- Task orchestration using Airflow  

---

## Website

**Website name:** Decathlon Kazakhstan  
**URL:** [https://decathlon.kz/](https://decathlon.kz/)

### Description

The selected website is a dynamic e-commerce platform where product data is rendered using JavaScript.  
Product listings, prices, and availability are loaded dynamically and require browser automation for correct data extraction.  
Simple HTTP requests cannot reliably retrieve the full dataset due to client-side rendering.

---

## Project Structure

```

project/
│   README.md
│   requirements.txt
│   airflow/
|   |---decathlon-dag.py
├── src/
│   ├── scraper.py
│   ├── cleaner.py
│   └── loader.py
└── data/
└── output.db
└── raw.json
└── clean.csv
└── cleaned.csv

````

---

## Data Collection

The scraper collects structured product data from the website using Selenium.

**Features:**

- Handles dynamic loading of product lists  
- Scrolls and navigates pages automatically  
- Extracts product names, prices, categories, and URLs  
- Saves raw data for further preprocessing  

To run scraping manually:

```bash
python src/scraper.py
````

Minimum dataset size after cleaning: 100 records.

---

## Data Cleaning and Preprocessing

The following steps are applied:

* Removal of duplicate records
* Handling of missing values
* Text normalization
* Conversion of prices and numeric fields
* Filtering of incomplete or invalid records

To run cleaning:

```bash
python src/cleaner.py
```

---

## Database Storage

The cleaned data is stored in a SQLite database file:

```
data/output.db
```

### Example Table Schema

| Column   | Description         |
| -------- | ------------------- |
| url       | Url link   |
| name     | Product name        |
| price    | Numeric price value |
| sku | SKU product    |
| image      | Image link   |

To load data into database:

```bash
python src/loader.py
```

Table creation logic is implemented inside the loader script.

---

## Automation with Apache Airflow

The full pipeline is automated using Apache Airflow.

The DAG performs:

1. Scraping data from the website
2. Cleaning the dataset
3. Loading into SQLite database

**DAG file:** `decathlon-dag.py`

Scheduled execution interval is no more than once every 24 hours.

---

## Running Apache Airflow

Initialize and start Airflow:

```bash
airflow db reset
airflow webserver --port 8080
airflow scheduler
```

Open in browser:

[http://localhost:8080](http://localhost:8080)

Enable the DAG and trigger manually or wait for scheduled execution.

---

## Expected Output

After successful execution:

* SQLite database file is created
* Table is populated with cleaned data
* Logs show execution of all steps
* At least one successful DAG run is visible in Airflow UI

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

**Tools and technologies used:**

* Python
* Selenium
* SQLite3
* Apache Airflow

---

## Academic Integrity

All code in this repository was written by the team without using AI tools.
No third-party templates or scripts were copied.
The project is fully original work.

The team can explain:

* Scraping logic
* Data preprocessing steps
* Database schema
* Airflow DAG structure
* Execution logs

---

## Team Members

* Begali Dinmukhammed
* Batyrbek Raiymbek


---

## Oral Defense

**Date:** December 5, 2025

The team is prepared to demonstrate:

* End-to-end pipeline
* Scraping process
* Database content
* Airflow workflow and logs

