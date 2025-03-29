from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json

# Define the DAG
with DAG(
    dag_id="NASA_APOD_Postgres",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    # Step 1: Create Table if it doesn't exist
    @task
    def create_table():
        ## Initialize Postgres Hook
        pg_hook = PostgresHook(postgres_conn_id="my_postgres_connection")

        # SQL query to create the table
        create_table_query = """
            CREATE TABLE IF NOT EXISTS apod_data(
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                explanation TEXT,
                url TEXT,
                date DATE,
                media_type VARCHAR(50) 
            );
        """

        # Executing the table creation query
        pg_hook.run(create_table_query)

    # Step 2: Fetch data from NASA APOD API


    # Step 3: Transform the data (Pick the information I need to save)


    # Step 4: Load the data into PostgreSQL Database


    # Step 5: Verify the data using DBViewer


    # Step 6: Define the task dependencies