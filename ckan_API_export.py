import os
import requests
import json
import re
from datetime import datetime  # Import the datetime module

# Prompt the user for the catalog URL
catalog_url = input("Enter the catalog URL from which you want to export datasets: ")
catalog_name = catalog_url.split('//')[1].split('/')[0].replace('.', '_')

# CKAN API endpoint for searching datasets
url = f"{catalog_url}/api/3/action/package_search"

# Ask the user whether to export all datasets, specific number, or specific datasets
export_choice = input("Do you want to export all datasets, specific number of datasets, or specific datasets? "
                      "(Type 'all', 'number', or 'specific'): ").lower()

# Initialize num_datasets
num_datasets = 0

if export_choice == 'number':
    # Prompt the user for the number of datasets to export
    try:
        num_datasets = int(input("Enter the number of datasets to export: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        exit()

# List datasets for selection if exporting specific datasets
selected_datasets = []
if export_choice == 'specific':
    print("Fetching datasets for selection...")
    response = requests.get(url, params={'q': '*:*', 'start': 0, 'rows': 10})
    if response.status_code == 200:
        datasets = response.json().get('result', {}).get('results', [])
        if not datasets:
            print("No datasets found.")
            exit()

        print("Available datasets:")
        for i, dataset in enumerate(datasets):
            print(f"{i + 1}. {dataset.get('title', 'unknown_title')}")

        # Prompt user to select datasets
        selected_datasets_indices = input("Enter the indices of the datasets you want to export (comma-separated): ")
        selected_indices = [int(index.strip()) - 1 for index in selected_datasets_indices.split(',')]

        # Filter datasets based on user selection
        selected_datasets = [datasets[i] for i in selected_indices]
    else:
        print(f"Error fetching datasets: {response.status_code}, {response.text}")
        exit()

# Ask the user whether to export all datasets into a single file or as separate files
export_option = input("Do you want to export all datasets into a single file? (yes/no): ").lower()

# Create the 'export' folder if it doesn't exist
export_folder = 'export'
os.makedirs(export_folder, exist_ok=True)

# Initialize the params dictionary
params = {
    'q': '*:*',  # Search query to retrieve all datasets
    'start': 0,
    'rows': 10,  # Number of datasets to retrieve per request (adjust as needed)
}

def clean_filename(filename):
    # Remove or replace invalid characters in the filename
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def ask_overwrite(existing_filename, new_filename):
    response = input(f"Dataset '{existing_filename}' already exists. Do you want to overwrite it? (yes/no): ").lower()
    return response == 'yes'

datasets_exported = 0

# Get the current date and time
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

# Define the export file or folder based on user's choice
if export_option == 'yes':
    # Construct the export filename with date and time
    export_filename = os.path.join(export_folder, f'{catalog_name}_all_datasets_{current_datetime}.json')
    export_all_datasets = True
else:
    export_all_datasets = False

for dataset in selected_datasets if export_choice == 'specific' else []:
    dataset_title = dataset.get('title', 'unknown_title')
    dataset_title_cleaned = clean_filename(dataset_title)

    if export_all_datasets:
        with open(export_filename, 'a' if datasets_exported > 0 else 'w') as export_file:
            json.dump(dataset, export_file, indent=2)
            export_file.write('\n')  # Add a newline between datasets
        print(f"Dataset '{dataset_title}' exported to {export_filename}")
    else:
        dataset_filename = os.path.join(export_folder, f'{dataset_title_cleaned}_{current_datetime}.json')

        # Check if the file already exists
        if os.path.exists(dataset_filename):
            if ask_overwrite(dataset_filename, dataset_title_cleaned):
                with open(dataset_filename, 'w') as dataset_file:
                    json.dump(dataset, dataset_file, indent=2)
                print(f"Dataset '{dataset_title}' overwritten in {dataset_filename}")
            else:
                # Append a unique index to the filename
                index = 1
                while os.path.exists(dataset_filename):
                    dataset_filename = os.path.join(export_folder, f'{dataset_title_cleaned}_{index}_{current_datetime}.json')
                    index += 1

                with open(dataset_filename, 'w') as dataset_file:
                    json.dump(dataset, dataset_file, indent=2)
                print(f"Dataset '{dataset_title}' exported to {dataset_filename}")
        else:
            with open(dataset_filename, 'w') as dataset_file:
                json.dump(dataset, dataset_file, indent=2)
            print(f"Dataset '{dataset_title}' exported to {dataset_filename}")

    datasets_exported += 1

while True:
    # Making the API request
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extracting the list of datasets from the response
        datasets = response.json().get('result', {}).get('results', [])

        if not datasets:
            break  # No more datasets to retrieve

        # Save each dataset to a separate or single JSON file in the 'export' folder
        for dataset in datasets:
            if export_choice == 'all' or (export_choice == 'number' and datasets_exported < num_datasets):
                dataset_title = dataset.get('title', 'unknown_title')
                dataset_title_cleaned = clean_filename(dataset_title)

                if export_all_datasets:
                    with open(export_filename, 'a' if datasets_exported > 0 else 'w') as export_file:
                        json.dump(dataset, export_file, indent=2)
                        export_file.write('\n')  # Add a newline between datasets
                    print(f"Dataset '{dataset_title}' exported to {export_filename}")
                else:
                    dataset_filename = os.path.join(export_folder, f'{dataset_title_cleaned}_{current_datetime}.json')

                    # Check if the file already exists
                    if os.path.exists(dataset_filename):
                        if ask_overwrite(dataset_filename, dataset_title_cleaned):
                            with open(dataset_filename, 'w') as dataset_file:
                                json.dump(dataset, dataset_file, indent=2)
                            print(f"Dataset '{dataset_title}' overwritten in {dataset_filename}")
                        else:
                            # Append a unique index to the filename
                            index = 1
                            while os.path.exists(dataset_filename):
                                dataset_filename = os.path.join(export_folder, f'{dataset_title_cleaned}_{index}_{current_datetime}.json')
                                index += 1

                            with open(dataset_filename, 'w') as dataset_file:
                                json.dump(dataset, dataset_file, indent=2)
                            print(f"Dataset '{dataset_title}' exported to {dataset_filename}")
                    else:
                        with open(dataset_filename, 'w') as dataset_file:
                            json.dump(dataset, dataset_file, indent=2)
                        print(f"Dataset '{dataset_title}' exported to {dataset_filename}")

                datasets_exported += 1

        # Move to the next set of datasets
        params['start'] += params['rows']

        if export_choice == 'number' and datasets_exported >= num_datasets:
            break  # Stop if the desired number of datasets is reached

    else:
        print(f"Error: {response.status_code}, {response.text}")
        break
