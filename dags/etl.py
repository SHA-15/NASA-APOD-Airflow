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
    # https://api.nasa.gov/planetary/apod?api_key=qyEa3P73bIRZpRNcDdtTofPTEl1O9CUWJEiAjJak
    extract_apod = SimpleHttpOperator(
        task_id="extract_apod",
        http_conn_id="nasa_api", # Connection ID defined in Airflow
        endpoint="planetary/apod", # Nasa API endpoint for astronomy picture of the day
        method="GET",
        data={"api_key":"{{ conn.nasa_api.extra_dejson.api_key }}"}, # Using the API key from the connection
        response_filter = lambda response: response.json() # Convert response to JSON
    )

    # Step 3: Transform the data (Pick the information I need to save)
    @task
    def transform_apod_data(response):
        apod_data = {
            "title": response.get("title", ""),
            "explanation": response.get("explanation", ""),
            "url": response.get("url", ""),
            "date": response.get("date", ""),
            "media_type": response.get("media_type", "")
        }

        return apod_data

    # Step 4: Load the data into PostgreSQL Database
    @task
    def load_to_postgres(apod_data):
        pg_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
    
        # Define the SQL insert query
        insert_query = """
            INSERT INTO apod_data (title, explanation, url, date, media_type)
            VALUES (%s, %s, %s, %s, %s)
        """

        # Execute the insert SQL query
        pg_hook.run(insert_query, parameters=(
            apod_data["title"],
            apod_data["explanation"],
            apod_data["url"],
            apod_data["date"],
            apod_data["media_type"]
        ))

    # Step 5: Verify the data using DBViewer


    # Step 6: Define the task dependencies
    create_table() >> extract_apod # Ensure table is created before data extraction
    api_response = extract_apod.output
    transformed_data = transform_apod_data(api_response)
    load_to_postgres(transformed_data)