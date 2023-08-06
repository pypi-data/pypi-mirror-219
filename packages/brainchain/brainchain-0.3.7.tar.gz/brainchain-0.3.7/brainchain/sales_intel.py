import requests
import os

class SalesIntel:
    def __init__(self, api_key):
        self.api_key = api_key or os.environ['SALESINTEL_API_KEY']
        self.base_url = "https://api.salesintel.io"

    def get_company(self, company_domain=None, company_industries=None, company_location_states=None,
                    company_location_zipcodes=None, company_location_zipcodes_distance=None,
                    company_max_revenue=None, company_max_size=None, company_min_revenue=None,
                    company_min_size=None, company_naics_codes=None, company_name=None,
                    company_sic_codes=None, email=None, first_name=None, is_ev_contact=None,
                    is_international=None):
        url = f"{self.base_url}/service/company"
        params = {
            "company_domain": company_domain,
            "company_industries": company_industries,
            "company_location_states": company_location_states,
            "company_location_zipcodes": company_location_zipcodes,
            "company_location_zipcodes_distance": company_location_zipcodes_distance,
            "company_max_revenue": company_max_revenue,
            "company_max_size": company_max_size,
            "company_min_revenue": company_min_revenue,
            "company_min_size": company_min_size,
            "company_naics_codes": company_naics_codes,
            "company_name": company_name,
            "company_sic_codes": company_sic_codes,
            "email": email,
            "first_name": first_name,
            "is_ev_contact": is_ev_contact,
            "is_international": is_international
        }
        headers = {"X-CB-ApiKey": f"{self.api_key}"}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_people(self, first_name=None, last_name=None, location_country_codes=None, page=1, page_size=50,
                   sort_by=None, sort_direction=None, tech_category=None, tech_product=None,
                   tech_subcategory=None, tech_vendor=None, verified=None):
        url = f"{self.base_url}/service/people"
        params = {
            "first_name": first_name,
            "last_name": last_name,
            "location_country_codes": location_country_codes,
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by,
            "sort_direction": sort_direction,
            "tech_category": tech_category,
            "tech_product": tech_product,
            "tech_subcategory": tech_subcategory,
            "tech_vendor": tech_vendor,
            "verified": verified
        }
        headers = {"X-CB-ApiKey": f"{self.api_key}"}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_technologies(self, company_domain=None, company_industries=None, company_location_states=None,
                         company_location_zipcodes=None, company_location_zipcodes_distance=None,
                         company_max_revenue=None, company_max_size=None, company_min_revenue=None,
                         company_min_size=None, company_naics_codes=None, company_name=None,
                         company_sic_codes=None, email=None, first_name=None, is_ev_contact=None,
                         is_international=None, job_departments=None, job_levels=None,
                         job_sub_departments=None, job_title=None, last_name=None,
                         location_country_codes=None, page=1, page_size=50, sort_by=None,
                         sort_direction=None, tech_category=None, tech_product=None,
                         tech_subcategory=None, tech_vendor=None, verified=None):
        url = f"{self.base_url}/service/technologies"
        params = {
            "company_domain": company_domain,
            "company_industries": company_industries,
            "company_location_states": company_location_states,
            "company_location_zipcodes": company_location_zipcodes,
            "company_location_zipcodes_distance": company_location_zipcodes_distance,
            "company_max_revenue": company_max_revenue,
            "company_max_size": company_max_size,
            "company_min_revenue": company_min_revenue,
            "company_min_size": company_min_size,
            "company_naics_codes": company_naics_codes,
            "company_name": company_name,
            "company_sic_codes": company_sic_codes,
            "email": email,
            "first_name": first_name,
            "is_ev_contact": is_ev_contact,
            "is_international": is_international,
            "job_departments": job_departments,
            "job_levels": job_levels,
            "job_sub_departments": job_sub_departments,
            "job_title": job_title,
            "last_name": last_name,
            "location_country_codes": location_country_codes,
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by,
            "sort_direction": sort_direction,
            "tech_category": tech_category,
            "tech_product": tech_product,
            "tech_subcategory": tech_subcategory,
            "tech_vendor": tech_vendor,
            "verified": verified
        }
        headers = {"X-CB-ApiKey": f"{self.api_key}"}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_news(self, last_name=None, location_country_codes=None, page=1, page_size=50,
                 sort_by=None, sort_direction=None, tech_category=None, tech_product=None,
                 tech_subcategory=None, tech_vendor=None, verified=None):
        url = f"{self.base_url}/service/news"
        params = {
            "last_name": last_name,
            "location_country_codes": location_country_codes,
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by,
            "sort_direction": sort_direction,
            "tech_category": tech_category,
            "tech_product": tech_product,
            "tech_subcategory": tech_subcategory,
            "tech_vendor": tech_vendor,
            "verified": verified
        }
        headers = {"X-CB-ApiKey": f"{self.api_key}"}
        response = requests.get(url, headers=headers, params=params)
        return response.json()
