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

# Function to convert user data to a DataFrame
def users_to_dataframe(users):
    data = []
    for user in users:
        user_data = {
            "ID": user.get("id", ""),
            "Name": user.get("name", ""),
            "Email": user.get("email", ""),
            "State": user.get("state", ""),
            "Created": user.get("created", ""),
            "Last Modified": user.get("last_modified", "")
        }
        data.append(user_data)
    return pd.DataFrame(data)

# Main script
if __name__ == "__main__":
    users = get_all_users()
    if users:
        df = users_to_dataframe(users)
        output_file = "ckan_users.xlsx"
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"User data has been written to {output_file}")
    else:
        print("No user data available to write.")
