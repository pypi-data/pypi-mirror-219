import os
import sys
import json
import requests
from urllib.parse import quote
from . import SalesIntel, FactCheck

class Brainchain:
    def __init__(self, env: str = "prod", api_key: str = os.environ["BRAINCHAIN_API_KEY"], service_url="https://brainchain--agent.modal.run/", salesintel_api_key=os.environ["SALESINTEL_API_KEY"]):
        self.api_key = api_key
        self.env = env
        self.fact_check_instance = FactCheck(environment=env)
        self.sales_intel_client = SalesIntel(salesintel_api_key)
        self.environments = ["prod", "dev"]
        self.services = {
            "agent": {
                "prod": "https://brainchain--agent.modal.run/",
                "dev": "https://brainchain--agent-dev.modal.run/"
            },
            "prompt-completion-service": {
                "prompting": "https://brainchain--prompt-completion-service-fastapi-app.modal.run/prompting",
                "get_pdf_title": "https://brainchain--prompt-completion-service-fastapi-app.modal.run/get_pdf_title",
                "get_pdf_authors": "https://brainchain--prompt-completion-service-fastapi-app.modal.run/get_pdf_authors"
            },
            "search": {
                "prod": "https://brainchain--search.modal.run/",
                "dev":  "https://brainchain--search-dev.modal.run/"
            },
            "electrolaser": {
                "prod": "https://brainchain--electrolaser.modal.run/",
                "dev": "https://brainchain--electrolaser-dev.modal.run/"
            }
        }

    def fact_check(self, statement):
        return self.fact_check_instance.fact_check(statement)

    def search(self, query):
        endpoint = self.services["search"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query}
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def search_results(self, query: str, additional_pages: int = 10):
        return self.electrolaser(query, additional_pages=additional_pages)

    def electrolaser(self, query: str, additional_pages: int = 50):
        endpoint = self.services["electrolaser"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query, "additional_pages": additional_pages}
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def bullet_point_summarizer(self, text: str, prompt=""):
        endpoint = self.services["electrolaser"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query, "additional_pages": additional_pages}
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def prompt(self, q, history=[], top_p=0.0, system="You are a multi-disciplinary research assistant who formulates, validates, and figures out correct answers. Your insights are ferocious and undeniable. You expand and digest new concepts and relate them to what you already know.", model="gpt-3.5-turbo-16k", presence_penalty=0.0, frequency_penalty=0.0, n=1):
        endpoint = self.services["prompt-completion-service"]["prompting"]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"user_prompt": q, "history": history, "system_prompt": system, "model": model, "presence_penalty": float(
            presence_penalty), "frequency_penalty": float(frequency_penalty), "top_p": float(top_p)}
        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def obtain_title(self, text_first_page: str = None):
        endpoint = self.services["prompt-completion-service"]["get_pdf_title"]
        payload = {}

        if text_first_page:
            payload["document_text"] = text_first_page
    
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(endpoint, headers=headers, json=payload)
        content = response.content.decode('utf-8')
        return json.loads(content)

    def obtain_authors(self, text_first_page: str = None):
        endpoint =  self.services["prompt-completion-service"]["get_pdf_authors"]
        payload = {}

        if text_first_page:
            payload["document_text"] = text_first_page

        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(endpoint, headers=headers, json=payload)
        content = response.content.decode('utf-8')
        return json.loads(content)

    def summon(self, prompt, agent_type="CCR", model="gpt-4-0613", max_tokens=2048, temperature=0.18, top_p=0.15, top_k=0.0, presence_penalty=1.0, frequency_penalty=1.0):
        endpoint = self.services["agent"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "prompt": prompt,
            "env": self.env,
            "agent_type": agent_type,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty
        }
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_company(self, **kwargs):
        return self.sales_intel_client.get_company(**kwargs)

    def get_people(self, **kwargs):
        return self.sales_intel_client.get_people(**kwargs)

    def get_technologies(self, **kwargs):
        return self.sales_intel_client.get_technologies(**kwargs)

    def get_news(self, **kwargs):
        return self.sales_intel_client.get_news(**kwargs)
