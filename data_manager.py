import os
from pprint import pprint
import requests

SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
TOKEN = os.environ["SHEETY_TOKEN"]

class DataManager:

    def __init__(self):
        self.users_data = {}
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=f"{SHEETY_ENDPOINT}/prices", headers={"Authorization": TOKEN})
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            print(f"{SHEETY_ENDPOINT}/prices/{city['id']}")
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/prices/{city['id']}",
                json=new_data,
                headers={"Authorization": TOKEN}
            )
            print(response.text)

    def get_emails(self):
        response = requests.get(url=f"{SHEETY_ENDPOINT}/users", headers={"Authorization": TOKEN})
        data = response.json()
        self.users_data = data["users"]
        emails = [user["email"] for user in self.users_data]
        return emails

