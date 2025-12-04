import sys
import os
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import logging

# ----------------------------------------
# Добавляем путь к проекту, чтобы импортировать scraper/cleaner/loader
# ----------------------------------------
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(PROJECT_PATH)

# Теперь можно импортировать твои файлы
from scraper import scrape_list_page
from cleaner import clean_data
from loader import load_data

# ----------------------------------------
# Default args
# ----------------------------------------
default_args = {
    "owner": "din",
    "retries": 2,
    "retry_delay": timedelta(minutes=3),
}

# ----------------------------------------
# DAG definition
# ----------------------------------------
dag = DAG(
    dag_id="decathlon_pipeline",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=timedelta(hours=24),
    catchup=False,
)

# ----------------------------------------
# TASK 1 — SCRAPER
# ----------------------------------------
def run_scraper():
    logging.info("Starting SCRAPER...")
    start_url = "https://decathlon.kz/142-futbol"
    scrape_list_page(start_url, headless=True, min_items=150)
    logging.info("SCRAPER finished. Saved → data/raw.json")


scraper_task = PythonOperator(
    task_id="scrape_products",
    python_callable=run_scraper,
    dag=dag,
)

# ----------------------------------------
# TASK 2 — CLEANER
# ----------------------------------------
def run_cleaner():
    logging.info("Starting CLEANER...")
    clean_data("data/raw.json", "data/clean.json")
    logging.info("CLEANER finished. Saved → data/clean.json")


cleaner_task = PythonOperator(
    task_id="clean_products",
    python_callable=run_cleaner,
    dag=dag,
)

# ----------------------------------------
# TASK 3 — LOADER
# ----------------------------------------
def run_loader():
    logging.info("Starting LOADER...")
    load_data("data/clean.json")
    logging.info("LOADER finished. Load completed.")


loader_task = PythonOperator(
    task_id="load_products",
    python_callable=run_loader,
    dag=dag,
)

# ----------------------------------------
# PIPELINE ORDER
# ----------------------------------------
scraper_task >> cleaner_task >> loader_task
