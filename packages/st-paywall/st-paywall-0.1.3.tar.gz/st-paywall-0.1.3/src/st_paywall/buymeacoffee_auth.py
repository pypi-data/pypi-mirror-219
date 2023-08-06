import requests
import streamlit as st
bmac_api = st.secrets["bmac_api_key"]

def extract_payer_emails(json_response):
    payer_emails = []

    for item in json_response['data']:
        payer_email = item['payer_email']
        payer_emails.append(payer_email)

    return payer_emails

def get_bmac_payers(access_token=bmac_api, one_time=False):
    if one_time == False:
        url = "https://developers.buymeacoffee.com/api/v1/subscriptions?status=active"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return extract_payer_emails(response.json())
        else:
            raise Exception(f"Error fetching active subscriptions: {response.status_code} - {response.text}")
    else:
        url = "https://developers.buymeacoffee.com/api/v1/supporters"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return extract_payer_emails(response.json())
        else:
            raise Exception(f"Error fetching active subscriptions: {response.status_code} - {response.text}")