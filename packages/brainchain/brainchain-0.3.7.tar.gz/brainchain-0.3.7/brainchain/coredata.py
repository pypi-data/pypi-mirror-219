import json, os, requests
from typing import Any, Dict

class CoreData:
    endpoints = {
        "create_table": {"method": "POST", "params": ["table"]},
        "insert_row": {"method": "POST", "params": ["table_name", "row_data"]},
        "get_metadata": {"method": "GET", "params": []},
        "delete_row": {"method": "POST", "params": ["table_name", "row_id"]},
        "update_row": {"method": "POST", "params": ["table_name", "row_id", "row_data"]},
        "get_all_rows": {"method": "GET", "params": ["table_name"]},
        "get_row": {"method": "GET", "params": ["table_name", "row_id"]},
        "drop_table": {"method": "POST", "params": ["table_name"]},
        "count_rows": {"method": "GET", "params": ["table_name"]},
        "query_by_column": {"method": "GET", "params": ["table_name", "column_name", "column_value"]},
        "migrate_schema": {"method": "POST", "params": ["table", "new_columns"]},
        "run_raw_sql": {"method": "POST", "params": ["query"]}
    }

    def __init__(self, api_key=os.getenv("COREDATA_API_KEY"), env="prod"):
        self.env = "test"
        self.token = api_key or os.getenv("COREDATA_API_KEY")
        for endpoint, info in self.endpoints.items():
            self.generate_method(endpoint, info)

    def get_url(self, endpoint: str) -> str:
        if self.env == "prod":
            return f"https://brainchain--{endpoint}.modal.run"
        if self.env == "test":
            return f"https://brainchain--{endpoint}.modal.run"
        if self.env == "dev":  # Assuming any other value refers to a dev environment
            return f"https://brainchain--{endpoint}-dev.modal.run"

    def generate_method(self, endpoint, info):
        def method(*args, **kwargs):
            url = self.get_url(endpoint.replace("_", "-"))
            params = {param: kwargs.get(param) for param in info["params"]}
            print(params)
            headers = {'Authorization': f'Bearer {self.token}'}
            if info["method"] == "GET":
                response = requests.get(url, params=params, headers=headers)
            else:
                response = requests.post(url, json=params, headers=headers)
            return response.json()

        setattr(self, endpoint, method)
