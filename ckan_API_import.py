import os
import json
import requests

def import_to_ckan(api_url, api_key, file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        dataset_data = json.load(file)

    # Set the CKAN API endpoint
    endpoint = f'{api_url}/api/3/action/package_create'

    # Set the CKAN API key for authorization
    headers = {'Authorization': api_key, 'Content-Type': 'application/json'}

    # Make the API request to create the dataset
    response = requests.post(endpoint, json=dataset_data, headers=headers)

    # Check the response
    if response.status_code == 200:
        print('Dataset successfully imported to CKAN!')
    else:
        print('Failed to import dataset. Response:', response.text)

def list_files_in_path(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return files

if __name__ == '__main__':
    # CKAN API URL (replace with your CKAN instance URL)
    ckan_api_url = 'http://localhost:5000/'

    # CKAN API key for authorization (replace with your API key)
    ckan_api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjTzE3WWNqU2pycldCZWRkQzdmZlFvVGV6aUpNam94a0pPV08tZnFzMHM5bjRZWDhWRnlhaVd6V1dubWp3LXNuazdEVGJKNWlhQ2VaQjVGaSIsImlhdCI6MTcwMjY1NTYxOH0.Rpudi4WItUJ6nDN24BPODVLqcR_2aPwuCDqr_BbjZr8'

    # Ask the user for the directory path
    directory_path = input('Enter the path to the directory containing JSON files: ')

    # List available files in the directory
    files = list_files_in_path(directory_path)

    if not files:
        print('No JSON files found in the specified directory.')
    else:
        print('Available JSON files:')
        for i, file in enumerate(files, start=1):
            print(f'{i}. {file}')

        # Ask the user to choose a file
        file_choice = input('Enter the number of the file you want to import: ')

        try:
            file_choice = int(file_choice)
            if 1 <= file_choice <= len(files):
                chosen_file = os.path.join(directory_path, files[file_choice - 1])
                import_to_ckan(ckan_api_url, ckan_api_key, chosen_file)
            else:
                print('Invalid file number.')
        except ValueError:
            print('Invalid input. Please enter a number.')
