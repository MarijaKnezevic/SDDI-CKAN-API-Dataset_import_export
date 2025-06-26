import os
import requests
import json
import re
from datetime import datetime

# Prompt the user for the catalog URL
catalog_url = input("Enter the catalog URL from which you want to export datasets: ")
catalog_name = catalog_url.split('//')[1].split('/')[0].replace('.', '_')

# CKAN API endpoint for searching datasets
url = f"{catalog_url}/api/3/action/package_search"

# Ask the user whether to export all datasets, a specific number, or specific datasets
export_choice = input("Do you want to export all datasets, a specific number of datasets, or specific datasets? "
                      "(Type 'all', 'number', or 'specific'): ").lower()

# Initialize num_datasets
num_datasets = 0

if export_choice == 'number':
    try:
        num_datasets = int(input("Enter the number of datasets to export: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        exit()

selected_datasets = []
if export_choice == 'specific':
    print("Fetching datasets for selection...")
    response = requests.get(url, params={'q': '*:*', 'start': 0, 'rows': 1000})
    if response.status_code == 200:
        datasets = response.json().get('result', {}).get('results', [])
        if not datasets:
            print("No datasets found.")
            exit()

        print("Available datasets:")
        for i, dataset in enumerate(datasets):
            print(f"{i + 1}. {dataset.get('title', 'unknown_title')}")

        selected_indices = input("Enter the indices of the datasets you want to export (comma-separated): ")
        selected_indices = [int(index.strip()) - 1 for index in selected_indices.split(',')]
        selected_datasets = [datasets[i] for i in selected_indices]
    else:
        print(f"Error fetching datasets: {response.status_code}, {response.text}")
        exit()

# Ask the user whether to export into a single file or separate files
export_option = input("Do you want to export all datasets into a single file? (yes/no): ").lower()

# Create the export folder
export_folder = 'export'
os.makedirs(export_folder, exist_ok=True)

params = {
    'q': '*:*',
    'start': 0,
    'rows': 1000,
}

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def ask_overwrite(existing_filename, new_filename):
    response = input(f"Dataset '{existing_filename}' already exists. Overwrite? (yes/no): ").lower()
    return response == 'yes'

def download_resource(resource, save_dir, dataset_title_cleaned):
    resource_url = resource.get('url')
    resource_name = clean_filename(resource.get('name', 'resource'))
    resource_format = resource.get('format', '').lower()
    file_ext = f".{resource_format}" if resource_format else ""

    if resource_url and resource_url.startswith("http"):
        try:
            response = requests.get(resource_url, stream=True, timeout=10)
            response.raise_for_status()

            resource_filename = os.path.join(save_dir, f"{dataset_title_cleaned}_{resource_name}{file_ext}")
            base_filename = resource_filename
            index = 1
            while os.path.exists(resource_filename):
                resource_filename = f"{base_filename}_{index}{file_ext}"
                index += 1

            with open(resource_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Resource downloaded: {resource_filename}")
        except Exception as e:
            print(f"Failed to download resource from {resource_url}: {e}")

datasets_exported = 0
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

if export_option == 'yes':
    export_filename = os.path.join(export_folder, f'{catalog_name}_all_datasets_{current_datetime}.json')
    export_all_datasets = True
else:
    export_all_datasets = False

def export_dataset(dataset):
    global datasets_exported
    dataset_title = dataset.get('title', 'unknown_title')
    dataset_title_cleaned = clean_filename(dataset_title)

    if export_all_datasets:
        with open(export_filename, 'a' if datasets_exported > 0 else 'w') as export_file:
            json.dump(dataset, export_file, indent=2)
            export_file.write('\n')
        print(f"Dataset '{dataset_title}' exported to {export_filename}")
    else:
        dataset_filename = os.path.join(export_folder, f'{dataset_title_cleaned}_{current_datetime}.json')
        if os.path.exists(dataset_filename):
            if not ask_overwrite(dataset_filename, dataset_title_cleaned):
                index = 1
                while os.path.exists(dataset_filename):
                    dataset_filename = os.path.join(export_folder, f'{dataset_title_cleaned}_{index}_{current_datetime}.json')
                    index += 1
        with open(dataset_filename, 'w') as dataset_file:
            json.dump(dataset, dataset_file, indent=2)
        print(f"Dataset '{dataset_title}' exported to {dataset_filename}")

    # Download resources
    for resource in dataset.get('resources', []):
        download_resource(resource, export_folder, dataset_title_cleaned)

    datasets_exported += 1

# Export specific datasets
if export_choice == 'specific':
    for dataset in selected_datasets:
        export_dataset(dataset)

# Export 'all' or 'number' datasets
elif export_choice in ['all', 'number']:
    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            datasets = response.json().get('result', {}).get('results', [])
            if not datasets:
                break
            for dataset in datasets:
                if export_choice == 'number' and datasets_exported >= num_datasets:
                    break
                export_dataset(dataset)
            if export_choice == 'number' and datasets_exported >= num_datasets:
                break
            params['start'] += params['rows']
        else:
            print(f"Error: {response.status_code}, {response.text}")