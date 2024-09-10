import requests
import pandas as pd

# CKAN instance and API key
ckan_url = "http://your-ckan-instance-url" # Replace with your CKAN instance URL
api_key = "your-admin-api-key" # Replace with your CKAN API Key

# Function to get all users
def get_all_users():
    url = f"{ckan_url}/api/3/action/user_list"
    headers = {"Authorization": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        print(f"Error fetching users: {response.text}")
        return []

# Function to get all users
def get_all_users():
    url = f"{ckan_url}/api/3/action/user_list"
    headers = {"Authorization": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        print(f"Error fetching users: {response.text}")
        return []

# Function to get all users
def get_all_users():
    url = f"{ckan_url}/api/3/action/user_list"
    headers = {"Authorization": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        print(f"Error fetching users: {response.text}")
        return []

# Function to get user details by ID
def get_user_details(user_id):
    url = f"{ckan_url}/api/3/action/user_show"
    headers = {"Authorization": api_key}
    data = {"id": user_id}
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        print(f"Error fetching user details for {user_id}: {response.text}")
        return None

# Function to soft-delete a user (set 'state' to 'deleted')
def soft_delete_user(user_id):
    user_details = get_user_details(user_id)
    if user_details is None:
        return
    
    email = user_details.get("email", "")
    if not email:
        print(f"Error: User {user_id} does not have an email address.")
        return
    
    url = f"{ckan_url}/api/3/action/user_update"
    headers = {"Authorization": api_key}
    data = {"id": user_id, "state": "deleted", "email": email}
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"User {user_id} soft-deleted successfully.")
    else:
        print(f"Error soft-deleting user {user_id}: {response.text}")

# Function to find user ID by username
def get_user_id_by_username(username):
    users = get_all_users()
    for user in users:
        if user['name'] == username:
            return user['id']
    print(f"User with username {username} not found.")
    return None

# Main script
if __name__ == "__main__":
    # List of usernames to delete
    usernames_to_delete = ["brafixde", "brafixdea", "femarade", "xelodade", "lexaprode", "albendazolede", "nolvadexde", "norvascde", "torsemidede", "cabgolinde", "zofrande", "kepprade", "promethazinede", "propranololde", "furosemidede", "nitroglycerinde", "suhagrade", "combiventde", "vasotecde", "avodartde", "exelonde", "parietde", "prednisolonede", "dramaminede", "reminylde", "erythromycinde", "tofranilde", "wellbutrinsrde", "levothroidde", "supraxde", "zenegrade", "augmentinde", "diflucande", "ditropande", "dostinexde", "ventolinde", "ladyerade", "xenicalde", "colchicinede", "feldenede", "fucidinde", "zyprexade", "lasixde", "motiliumde", "doxycyclinede", "phenergande", "clozarilde", "bactrimde", "paroxetinede", "xalatande", "cytotecde", "indocinde", "advairdiskusde", "seroquelde", "elavilde", "adalatde", "parlodelde", "grifulvinvde", "tetracyclinede", "busparde", "metoclopramidede", "naprosynde", "synthroidde", "florinefde", "flomaxde", "clomidde", "trazodonede", "ranitidinede", "lisinoprilde", "zoviraxde", "zyvoxde", "proverade", "nexiumde", "sinequande", "tamoxifende", "toradolde", "anafranilde", "amantadinede", "ataraxde", "pletalde", "entocortde", "propeciade", "evistade", "betnovatede", "medrolde", "zoloftde", "unisomde", "stratterade", "robaxinde", "coumadinde", "voltarende", "zithromaxde", "yasminde", "desyrelde", "proscarde", "mestinonde", "effexorxrde", "stromectolde", "hytrinde", "reglande", "noroxinde", "pkhongcuog118"]  # Add usernames you want to delete here
    
    for username in usernames_to_delete:
        user_id = get_user_id_by_username(username)
        if user_id:
            soft_delete_user(user_id)
