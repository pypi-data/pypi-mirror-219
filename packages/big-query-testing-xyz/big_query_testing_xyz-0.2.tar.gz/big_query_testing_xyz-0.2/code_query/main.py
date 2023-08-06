from google.cloud import bigquery
import pandas as pd

credentials_path = '/Users/vedantrathi/Desktop/big_query_test/irsdata-pypi-4955991a9ae8.json'


project_id = 'irsdata-pypi'
dataset_id = 'dataset001'
table_id = 'vw_irs_filing_test02'
# table_id = 'irsdata-pypi.dataset001.irs_filing'


client = bigquery.Client.from_service_account_json(credentials_path)

sql_query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
# view_ref = client.dataset(dataset_id, project=project_id).table(table_id)
view_data = client.query(sql_query).to_dataframe()

# first_row = next(view_data)

# for field, value in first_row.items():
#     print(f"{field}: {value}")


def testing(index):
    return view_data.iloc[index]
