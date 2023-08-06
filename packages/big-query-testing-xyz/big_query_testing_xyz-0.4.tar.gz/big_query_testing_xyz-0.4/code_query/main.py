import io
import json
import requests
from google.cloud import bigquery
import pandas as pd

github_raw_url = 'https://raw.githubusercontent.com/vrathi101/big_query_testing_xyz/main/code_query/irs_api_credentials1.json'

try:
    response = requests.get(github_raw_url)
    response.raise_for_status()  # Raise an exception if the request was not successful
    content = response.content
except requests.exceptions.RequestException as e:
    print("Error occurred while retrieving the credentials:", e)
    # Perform error handling or raise the exception as needed
    raise

try:
    # Decode the content as a string
    credentials_str = content.decode('utf-8')

    # Load the credentials from the string
    credentials_dict = json.loads(credentials_str)

    # Use the loaded credentials in from_service_account_info
    client = bigquery.Client.from_service_account_info(credentials_dict)
except (json.JSONDecodeError, KeyError) as e:
    print("Error occurred while parsing the credentials:", e)
    # Perform error handling or raise the exception as needed
    raise

project_id = 'irsdata-pypi'
dataset_id = 'dataset001'
table_id = 'vw_irs_filing_test02'

try:
    sql_query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    view_data = client.query(sql_query).to_dataframe()
except Exception as e:
    print("Error occurred while querying BigQuery:", e)
    # Perform error handling or raise the exception as needed
    raise


def testing(index):
    try:
        return view_data.iloc[index]
    except IndexError as err:
        print("Error occurred while accessing the data at the specified index:", err)
        # Perform error handling or raise the exception as needed
        raise
    except Exception as err:
        print("An unexpected error occurred:", err)
        # Perform error handling or raise the exception as needed
        raise
